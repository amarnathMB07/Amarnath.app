import re
from typing import Any, Mapping


def _norm(text: str) -> str:
    t = text.strip().lower()
    t = re.sub(r"[\?\!\.\,\:\;\(\)\[\]\{\}\"\']", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _extract_crop_from_question(q: str) -> str | None:
    # Minimal extractor for common crops mentioned in the user’s question list.
    qn = _norm(q)
    for name in ("rice", "wheat", "tomato"):
        if re.search(rf"\b{name}\b", qn):
            return name.title()
    return None


_DEFINITIONS: dict[str, str] = {
    "crop rotation": (
        "Crop rotation means growing different crops on the same field in different seasons/years "
        "(for example: rice → pulses → vegetables)."
    ),
    "seasonal crops": (
        "Seasonal crops are crops grown in a particular season (summer, monsoon, or winter) "
        "because they match that season’s temperature and rainfall."
    ),
    "cash crops": (
        "Cash crops are grown mainly to sell for profit (for example: cotton, sugarcane, tea, coffee, spices)."
    ),
    "food crops": "Food crops are grown mainly for eating (for example: rice, wheat, maize, pulses, vegetables).",
    "crop yield": (
        "Crop yield is the amount of produce harvested from a given area, usually measured as kg/acre or tonnes/hectare."
    ),
    "hybrid seed": (
        "Hybrid seed is produced by crossing two selected parent lines to get higher yield or uniform plants. "
        "Hybrid seeds usually don’t breed true if you save and replant them."
    ),
    "organic farming": (
        "Organic farming uses natural inputs (compost, manure, bio-fertilizers) and biological pest control, "
        "and avoids synthetic chemical fertilizers and pesticides as much as possible."
    ),
    "sustainable farming": (
        "Sustainable farming aims to produce food while protecting soil, water, biodiversity, and farmer income "
        "over the long term (efficient water use, balanced nutrients, reduced chemicals)."
    ),
    "greenhouse farming": (
        "Greenhouse farming grows crops in a controlled structure where temperature, humidity, and pests can be managed."
    ),
    "mixed cropping": (
        "Mixed cropping means growing two or more crops together on the same land without a fixed row pattern, "
        "to reduce risk and improve resource use."
    ),
    "intercropping": (
        "Intercropping means growing two or more crops together in a planned row pattern (for example: maize + beans), "
        "to use sunlight, water, and nutrients efficiently."
    ),
    "seed germination": (
        "Seed germination is the process where a seed sprouts and starts growing into a new plant when it gets moisture, oxygen, and suitable temperature."
    ),
    "cover crops": (
        "Cover crops are grown mainly to protect and improve soil (reduce erosion, add organic matter, fix nitrogen), "
        "for example: sunn hemp, clover, cowpea."
    ),
    "perennial crops": "Perennial crops live for many years (for example: sugarcane, banana, coconut, mango, tea).",
    "annual crops": "Annual crops complete their life cycle in one season/year (for example: rice, wheat, maize, many vegetables).",
    "biennial crops": (
        "Biennial crops complete their life cycle in two years (often leaves/roots in year 1, flowers/seeds in year 2), "
        "for example: carrot, beetroot, onion (for seed production)."
    ),
    "irrigation": "Irrigation is the artificial supply of water to crops when rainfall is not enough.",
    "drip irrigation": "Drip irrigation delivers water slowly to the root zone through pipes/emitters, saving water and reducing weeds.",
    "sprinkler irrigation": "Sprinkler irrigation sprays water like rainfall using pipes and sprinkler heads.",
    "surface irrigation": "Surface irrigation spreads water over the field surface (furrows/basins).",
    "flood irrigation": "Flood irrigation covers the whole field with water; it is simple but can waste water and cause waterlogging.",
    "rainwater harvesting": "Rainwater harvesting collects and stores rainwater (farm ponds, tanks, recharge pits) for later use.",
    "irrigation scheduling": "Irrigation scheduling means deciding when and how much to irrigate based on crop stage, soil moisture, and weather.",
    "smart irrigation systems": "Smart irrigation systems use sensors, weather data, and controllers to irrigate only when needed.",
    "climate change": "Climate change is long-term change in temperature and rainfall patterns; it can increase heat stress, droughts, floods, and pest pressure.",
    "weather forecasting": "Weather forecasting predicts future weather (rain, temperature, wind). Farmers use it to plan irrigation, spraying, sowing, and harvest.",
    "drought": "Drought is a long period of low rainfall causing water shortage for crops.",
    "fertilizer": "Fertilizer is a material added to soil/plants to supply nutrients and improve growth.",
    "organic fertilizers": "Organic fertilizers come from natural sources like compost, manure, and bio-fertilizers.",
    "chemical fertilizers": "Chemical fertilizers are manufactured nutrient sources like urea, DAP, and NPK blends.",
    "npk fertilizer": "NPK fertilizer contains Nitrogen (N), Phosphorus (P), and Potassium (K) in a fixed ratio (example: 10-26-26).",
    "pest control": "Pest control means reducing damage from insects, weeds, and diseases using cultural, biological, mechanical, or chemical methods.",
    "biological pest control": "Biological pest control uses natural enemies (predators, parasites, beneficial microbes) to control pests.",
    "pesticide": "A pesticide is a chemical or biological agent used to control pests (insects, weeds, fungi). Use carefully and follow label instructions.",
    "integrated pest management": (
        "Integrated Pest Management (IPM) combines monitoring, resistant varieties, cultural methods, biological control, and careful pesticide use only when needed."
    ),
    "smart farming": "Smart farming uses technology (sensors, apps, automation, AI) to improve farm decisions and efficiency.",
    "precision agriculture": "Precision agriculture applies inputs (water, fertilizer) in the right amount, at the right place and time, using data and sensors.",
    "iot in agriculture": "IoT in agriculture means using connected sensors/devices to measure field conditions (soil moisture, weather) and automate actions.",
    "soil moisture sensor": "A soil moisture sensor measures how wet or dry the soil is, helping farmers schedule irrigation.",
    "remote sensing in agriculture": "Remote sensing uses satellite/drone images to monitor crops, moisture, and stress over large areas.",
    "drone farming": "Drone farming uses drones for mapping, monitoring, and sometimes spraying (where legal and safe).",
    "farm automation": "Farm automation uses machines and controllers to reduce manual work (auto-irrigation, fertigation, greenhouse controls).",
    "vertical farming": "Vertical farming grows crops in stacked layers (often indoors) with controlled light and nutrients.",
    "hydroponic farming": "Hydroponics grows plants without soil, using nutrient-rich water solutions.",
    "aquaponic farming": "Aquaponics combines fish farming and hydroponics; fish waste provides nutrients for plants, and plants help clean the water.",
}


_CROPS_BY_CLIMATE: dict[str, str] = {
    "hot": "Hot climates: millets (jowar/sorghum, bajra/pearl millet), maize, groundnut, cotton, sesame, some vegetables with irrigation.",
    "rainy": "Rainy/monsoon: rice (paddy), maize, soybean, groundnut, pulses (where drainage is good).",
    "cold": "Cold/cool climates: wheat, barley, mustard, peas, potato, temperate vegetables (cabbage/cauliflower).",
    "dry": "Dry regions: millets, pulses (chickpea/gram), groundnut, sesame, sorghum; use drought-tolerant varieties and drip irrigation.",
    "wet": "Wet/high-rain regions: rice, banana, tapioca, coconut, spices (pepper/cardamom) where suitable; prioritize drainage to prevent root diseases.",
    "summer": "Summer: maize, groundnut, sunflower, vegetables (tomato/okra) with irrigation.",
    "winter": "Winter: wheat, mustard, chickpea (gram), peas, many leafy vegetables.",
    "monsoon": "Monsoon: rice, maize, soybean, pulses depending on local rainfall and drainage.",
}


_SOIL_CROPS: dict[str, str] = {
    "sandy": "Sandy soil: groundnut, watermelon, coconut, carrots; needs frequent light irrigation and organic matter.",
    "clay": "Clay soil: rice, jute; can hold water well but needs good drainage/aeration for many crops.",
    "loamy": "Loamy soil: best for most crops (vegetables, wheat, maize, pulses) because it balances drainage and moisture retention.",
}


_REGION_CROPS: dict[str, str] = {
    "tamil nadu": "Tamil Nadu: rice, sugarcane, cotton, groundnut, millets, banana, coconut, turmeric; also vegetables in irrigated belts.",
    "kerala": "Kerala: coconut, rubber, banana, rice (paddy), tapioca, pepper, cardamom, tea/coffee (high ranges), spices and vegetables in suitable areas.",
}


def answer_question(question: str, crop: str, info: Mapping[str, Any]) -> str | None:
    qn = _norm(question)

    # --- Direct "what is ..." definitions ---
    m = re.match(r"^(what is|define)\s+(.+)$", qn)
    if m:
        term = m.group(2).strip()
        # normalize common trailing words
        term = re.sub(r"\?$", "", term).strip()
        term = term.replace("the ", "")
        if term in _DEFINITIONS:
            return _DEFINITIONS[term]

    # --- Crop durations ---
    if "how long" in qn and ("take" in qn or "takes" in qn) and ("grow" in qn or "harvest" in qn):
        asked_crop = _extract_crop_from_question(question) or crop
        if asked_crop.lower() == "rice":
            return "Rice typically takes about 120–150 days (variety and season can change this)."
        if asked_crop.lower() == "wheat":
            return "Wheat typically takes about 110–140 days (depends on variety and temperature)."
        if asked_crop.lower() == "tomato":
            return "Tomato typically takes about 60–90 days from transplanting to first harvest (variety and weather matter)."
        if info.get("harvest"):
            return f"{asked_crop} typical harvest time is {info.get('harvest')}."

    # --- Season / climate crop suggestions ---
    if "hot climate" in qn or ("hot" in qn and "climate" in qn):
        return _CROPS_BY_CLIMATE["hot"]
    if "rainy season" in qn or ("rainy" in qn and "season" in qn) or "monsoon" in qn:
        return _CROPS_BY_CLIMATE.get("monsoon") if "monsoon" in qn else _CROPS_BY_CLIMATE["rainy"]
    if "cold climate" in qn or ("cold" in qn and "climate" in qn) or "winter" in qn:
        return _CROPS_BY_CLIMATE.get("winter") if "winter" in qn else _CROPS_BY_CLIMATE["cold"]
    if "dry region" in qn or ("dry" in qn and "region" in qn):
        return _CROPS_BY_CLIMATE["dry"]
    if "wet region" in qn or ("wet" in qn and "region" in qn):
        return _CROPS_BY_CLIMATE["wet"]

    if "best to grow" in qn and "season" in qn:
        season = str(info.get("season") or "").strip()
        if season:
            return f"For the selected crop ({crop}), the recommended season is: {season}."
        return (
            "It depends on your local season and water availability. Tell me your location and month, "
            "or select a crop and I’ll use its season recommendation."
        )

    # --- Soil questions ---
    if "types of soil" in qn:
        return "Main soil types (basic): sandy, clay, silt, and loamy (a balanced mix)."
    if qn.startswith("what is sandy soil") or qn == "what is sandy soil":
        return "Sandy soil has large particles and drains fast. It warms quickly but holds less water and nutrients."
    if qn.startswith("what is clay soil") or qn == "what is clay soil":
        return "Clay soil has very small particles and holds water strongly. It can get waterlogged and needs good drainage/aeration."
    if qn.startswith("what is loamy soil") or qn == "what is loamy soil":
        return "Loamy soil is a balanced mix of sand/silt/clay. It holds moisture and nutrients while still draining well—good for most crops."
    if "soil is best for farming" in qn or ("best" in qn and "soil" in qn and "farming" in qn):
        return "Loamy soil is generally best for farming because it balances drainage, moisture retention, and nutrients."

    if "sandy soil" in qn and "crops" in qn:
        return _SOIL_CROPS["sandy"]
    if "clay soil" in qn and "crops" in qn:
        return _SOIL_CROPS["clay"]
    if "loamy soil" in qn and "crops" in qn:
        return _SOIL_CROPS["loamy"]

    if "soil moisture" in qn and qn.startswith("what is"):
        return "Soil moisture is the amount of water present in the soil. It affects germination, nutrient uptake, and root health."
    if "why is soil moisture important" in qn:
        return "Soil moisture controls plant water supply, nutrient movement, and root oxygen—too low causes stress, too high can cause rot/diseases."
    if "measure soil moisture" in qn:
        return (
            "Farmers measure soil moisture using feel-and-appearance, gravimetric testing (weigh/dry), "
            "or sensors like tensiometers, capacitance probes, or TDR."
        )

    if "ideal soil moisture" in qn:
        # Keep this simple and consistent with the app's 0–100% gauge (sensor-calibrated).
        if "rice" in qn:
            return "Rice prefers very wet soil—often near saturated/flooded. On a 0–100% moisture gauge, many farmers target ~70–90% (calibrate for your sensor)."
        if "wheat" in qn:
            return "Wheat prefers moderate moisture with good aeration. On a 0–100% moisture gauge, a common target is ~40–60% (calibrate for your sensor)."
        if "vegetable" in qn or "vegetables" in qn:
            return "Most vegetables prefer evenly moist (not waterlogged) soil. On a 0–100% moisture gauge, ~50–70% is a common target (calibrate for your sensor)."
        # Use selected crop if user didn’t specify.
        if crop.lower() == "rice":
            return "For the selected crop (Rice), keep soil very wet—often near saturated/flooded. Target ~70–90% on a 0–100% gauge (after calibration)."
        if crop.lower() == "wheat":
            return "For the selected crop (Wheat), keep soil moderately moist with good aeration. Target ~40–60% on a 0–100% gauge (after calibration)."
        return "Ideal soil moisture depends on the crop and soil type. Tell me the crop and your soil type for a better target."

    if "too low" in qn and "soil moisture" in qn:
        return "If soil moisture is too low, plants wilt, growth slows, flowers/fruit drop, and yield reduces."
    if "too high" in qn and "soil moisture" in qn:
        return "If soil moisture is too high, roots get less oxygen, causing yellowing, root rot, fungal disease, and nutrient loss."

    if "soil erosion" in qn and qn.startswith("what is"):
        return "Soil erosion is the removal of top fertile soil by water or wind."
    if "prevent" in qn and "soil erosion" in qn:
        return "Prevent soil erosion using cover crops, mulching, contour farming, terraces, bunds, reduced tillage, and windbreaks."
    if "soil testing" in qn and qn.startswith("what is"):
        return "Soil testing measures pH, organic matter, and nutrients (N, P, K and micronutrients) to guide fertilizer and soil amendments."
    if "why is soil testing important" in qn:
        return "Soil testing prevents over/under-fertilizing, saves money, improves yield, and protects soil and water from pollution."
    if "soil ph" in qn and qn.startswith("what is"):
        return "Soil pH shows how acidic or alkaline soil is. It affects nutrient availability and microbial activity."
    if "why is soil ph important" in qn:
        return "Wrong pH can lock nutrients in the soil. Correct pH helps crops absorb nutrients efficiently."

    if "macronutrients" in qn:
        return "Macronutrients are needed in large amounts: Nitrogen (N), Phosphorus (P), Potassium (K), plus Calcium, Magnesium, and Sulfur."
    if "micronutrients" in qn:
        return "Micronutrients are needed in small amounts: Iron, Zinc, Manganese, Copper, Boron, Molybdenum, Chlorine, Nickel."
    if qn.startswith("what is compost") or qn == "what is compost":
        return "Compost is decomposed organic matter (plant/animal waste) used to improve soil structure and nutrient supply."
    if "compost improve soil" in qn:
        return "Compost improves soil by increasing organic matter, water-holding capacity, beneficial microbes, and slow nutrient release."
    if "organic manure" in qn and qn.startswith("what is"):
        return "Organic manure is decomposed animal/plant waste (FYM, compost, poultry manure) used to add nutrients and organic matter."
    if "vermicompost" in qn and qn.startswith("what is"):
        return "Vermicompost is compost produced with earthworms; it’s rich in nutrients and beneficial microbes."
    if "earthworms" in qn and "help" in qn and "soil" in qn:
        return "Earthworms improve soil structure by making channels for air/water and converting organic matter into nutrient-rich castings."

    if "reduce soil pollution" in qn:
        return "Reduce soil pollution by using correct fertilizer doses (soil-test based), avoiding over-spraying pesticides, safe chemical storage, and adding organic matter."
    if "retain more water" in qn or ("soil" in qn and "retain" in qn and "water" in qn):
        return "To help soil retain water: add compost/FYM, use mulching, reduce tillage, grow cover crops, and improve soil structure."

    # Soil suitability for rice (keep old test expectation phrase).
    if "soil" in qn and crop.lower() == "rice":
        return "Rice prefers heavy, water-retentive soil and flooded conditions. Maintain high moisture for best results."

    # --- Irrigation / water ---
    if "types of irrigation" in qn:
        return "Common irrigation types: drip, sprinkler, surface (furrow/basin), and flood. Drip is most water-efficient."
    if "best time to water" in qn:
        return "Best time to water is early morning (or evening) to reduce evaporation and disease risk."
    if "save water" in qn or "reduce water waste" in qn or "water conservation" in qn:
        return "Save water using drip irrigation, mulching, irrigation scheduling (soil moisture + weather), fixing leaks, and rainwater harvesting."
    if "over irrigation" in qn:
        return "Over-irrigation can cause waterlogging, root diseases, nutrient leaching, and higher weed pressure."
    if "under irrigation" in qn:
        return "Under-irrigation causes wilting, poor flowering/fruiting, smaller produce, and lower yield."
    if "groundwater irrigation" in qn:
        return "Groundwater irrigation uses wells/borewells. Use it carefully to avoid depletion; combine with efficient methods like drip."
    if "canal irrigation" in qn:
        return "Canal irrigation supplies water through canals from rivers/reservoirs. It can be efficient but needs good scheduling and maintenance."
    if "irrigation efficiency" in qn:
        return "Irrigation efficiency is how much applied water is actually used by the crop. Drip is usually highest, flood is usually lowest."
    if "tools are used for irrigation" in qn:
        return "Common tools: pumps, pipes/valves, drip lines, sprinklers, timers/controllers, soil moisture sensors, and flow meters."
    if "how often should crops be watered" in qn:
        return "Watering frequency depends on crop stage, soil type, and weather. Sandy soils need more frequent light watering; clay soils need less frequent deeper watering."
    if "how much water do crops need" in qn:
        return "Water needs depend on crop, stage, and climate. Tell me the crop and your soil type (sandy/clay/loamy) for a better estimate."

    if "crops need more water" in qn:
        return "More water crops: rice (paddy), sugarcane, banana, many leafy vegetables (depending on climate)."
    if "crops need less water" in qn:
        return "Less water crops: millets, pulses (chickpea/gram), sesame, groundnut; use drought-tolerant varieties where possible."

    # --- Weather / climate ---
    if "weather affect crops" in qn:
        return "Weather affects germination, growth rate, water demand, flowering, pest/disease spread, and final yield."
    if "temperature affect" in qn:
        return "Temperature controls growth speed and stress. Too hot can cause flower drop; too cold can slow growth and damage tissues."
    if "rainfall affect" in qn:
        return "Rainfall affects soil moisture and irrigation need. Too much can cause flooding/disease; too little causes drought stress."
    if "humidity affect" in qn and "disease" in qn:
        return "High humidity often increases fungal diseases (leaf spots, blights). Good spacing, airflow, and timely sprays help."
    if "humidity affect plant growth" in qn:
        return "Humidity affects transpiration. Very low humidity increases water loss; very high humidity can reduce transpiration and increase disease risk."
    if "protect crops from heat" in qn:
        return "Protect from heat using mulching, timely irrigation, shade nets (for vegetables), and heat-tolerant varieties."
    if "protect crops from frost" in qn:
        return "Protect from frost with light irrigation before cold nights, smoke/fogging (where allowed), covering seedlings, and windbreaks."
    if "during drought" in qn or (qn.startswith("what happens") and "drought" in qn):
        return "During drought, plants suffer water stress, leaves curl/wilt, growth slows, and yield reduces. Efficient irrigation and mulching help."
    if "manage drought" in qn:
        return "Manage drought with mulching, drip irrigation, drought-tolerant crops/varieties, moisture conservation, and adjusting sowing dates."
    if "flood" in qn and qn.startswith("what is"):
        return "A flood in agriculture is excess water covering fields, causing oxygen shortage to roots and sometimes plant death."
    if "floods damage crops" in qn:
        return "Floods can suffocate roots, spread diseases, wash away nutrients, and physically damage plants."
    if "protect crops from heavy rain" in qn:
        return "Protect from heavy rain by improving drainage, raised beds for vegetables, staking plants, and avoiding fertilizer application just before storms."
    if "extreme weather" in qn:
        return "Extreme weather includes heatwaves, cold waves/frost, heavy rainfall, cyclones, drought, and hailstorms."
    if "adapt to climate change" in qn:
        return "Adapt using resilient varieties, diversified crops, efficient irrigation, soil organic matter improvement, weather-based advisories, and better drainage."
    if "tolerate drought" in qn:
        return "Drought-tolerant crops include millets (bajra/jowar), sorghum, pigeon pea, chickpea, sesame, and groundnut."
    if "tolerate flooding" in qn:
        return "Flood-tolerant crops include rice (paddy) and some forage crops; for vegetables, focus on raised beds and drainage."
    if "growing season" in qn:
        return "Growing season is the period when temperature and moisture are suitable for a crop to grow from planting to harvest."
    if "harvesting season" in qn:
        return "Harvesting season is the time when the crop reaches maturity and is ready to harvest (depends on sowing date, variety, and weather)."

    # --- Fertilizers / pests / technology ---
    if "nitrogen" in qn and "soil" in qn:
        return "Nitrogen (N) supports leafy growth. Too little causes pale leaves; too much can cause excessive vegetative growth and lodging."
    if "phosphorus" in qn and "soil" in qn:
        return "Phosphorus (P) supports root growth, flowering, and energy transfer. Deficiency can cause poor rooting and delayed maturity."
    if "potassium" in qn and "soil" in qn:
        return "Potassium (K) improves stress tolerance, water regulation, and fruit quality. Deficiency can cause leaf edge scorch and weak stems."
    if "how often should fertilizer" in qn:
        return "Fertilizer timing depends on crop stage. Many crops use split doses (basal + top dressing). Soil testing gives the best plan."
    if "too much fertilizer" in qn:
        return "Too much fertilizer can burn roots, increase pests/diseases, cause lodging, and pollute water through nutrient runoff."
    if "common crop pests" in qn:
        return "Common pests include aphids, stem borers, bollworms, whiteflies, thrips, and cutworms (varies by crop and region)."
    if "natural pest control" in qn:
        return "Natural pest control includes neem-based sprays, pheromone traps, yellow sticky traps, beneficial insects, crop rotation, and field sanitation."
    if "identify plant diseases" in qn:
        return "Identify diseases by symptoms (spots, wilting, mold), crop stage, and weather. Photos + local agri officer/extension help confirm."
    if "prevent plant diseases" in qn:
        return "Prevent diseases with resistant varieties, proper spacing/airflow, crop rotation, clean seed, balanced nutrition, and avoiding overhead watering at night."
    if "ai help farmers" in qn:
        return "AI can help with disease detection from photos, irrigation scheduling, yield prediction, and advisory recommendations based on weather and sensors."
    if "technology increase crop yield" in qn:
        return "Technology improves yield through better irrigation control, soil testing, pest alerts, precision fertilizer use, and timely weather-based decisions."
    if "future trends" in qn or "future trends in agriculture" in qn:
        return "Future trends include precision irrigation, sensor-based advisory, drones, climate-resilient varieties, protected cultivation, and data-driven farm management."

    # --- Region-specific crops ---
    if "tamil nadu" in qn:
        return _REGION_CROPS["tamil nadu"]
    if "kerala" in qn:
        return _REGION_CROPS["kerala"]

    # --- Sunlight / temperature / growth factors ---
    if "factors affect plant growth" in qn:
        return "Main factors: sunlight, temperature, water, nutrients, soil type/pH, pests/diseases, spacing, and crop variety."
    if "how much sunlight" in qn or "need more sunlight" in qn:
        return "Most fruiting crops (tomato, chilli, brinjal) need full sun (~6–8 hours/day). Leafy greens tolerate partial shade."
    if "best temperature for crop growth" in qn or ("temperature" in qn and "ideal" in qn):
        if info.get("temp"):
            return f"For the selected crop ({crop}), the optimal temperature range is {info.get('temp')}°C."
        return "Ideal temperature depends on the crop. Select a crop in the app and I’ll use its optimal temperature range."
    if "stages of crop growth" in qn:
        return "Typical stages: seed germination → seedling → vegetative growth → flowering → fruit/seed development → maturity/harvest."

    # --- Profit / crop categories ---
    if "most profitable crops" in qn:
        return (
            "Profit depends on local market, costs, and risk. Often profitable options include vegetables, flowers, spices, "
            "fruits, and plantation crops—but check demand, storage, and price volatility in your area."
        )
    if "common vegetable crops" in qn:
        return "Common vegetables: tomato, onion, brinjal (eggplant), okra, chilli, cabbage, cauliflower, gourds, leafy greens."
    if "common fruit crops" in qn:
        return "Common fruits: banana, mango, papaya, guava, grapes, watermelon, pomegranate (depends on region)."
    if "plantation crops" in qn:
        return "Plantation crops are long-duration crops grown on large estates, for example: tea, coffee, rubber, coconut, cocoa."

    # --- Yield measurement ---
    if "measure crop yield" in qn:
        return "Farmers measure yield as harvested weight per area (kg/acre or tonnes/hectare). They sample plots, weigh produce, then scale to the full area."

    # --- Soil quality / fertility / diversification ---
    if "increase crop yield" in qn:
        return (
            "Increase yield by using quality seed, correct sowing time, soil testing, balanced nutrients (NPK + micronutrients), "
            "timely irrigation, weed control, pest/disease monitoring, and good spacing."
        )
    if "improve soil quality" in qn or "improve soil fertility" in qn:
        return "Improve soil with compost/FYM, green manure/cover crops, crop rotation, reduced tillage, and correcting pH based on soil test."
    if "benefits of crop diversification" in qn:
        return "Diversification reduces risk, improves soil health, breaks pest cycles, and can improve income stability."
    if "hybrid and local seeds" in qn or "difference between hybrid and local seeds" in qn:
        return "Hybrid seeds are high-yield but often need more inputs and saved seed may not perform the same. Local/open-pollinated seeds are more stable for saving and may be better adapted locally."
    if "select good seeds" in qn:
        return "Select good seeds by checking purity, germination rate, seed treatment, source certification, and choosing varieties suitable for your season and soil."

    return None

