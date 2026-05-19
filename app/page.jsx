import Hero from "@/components/Hero";
import About from "@/components/About";
import Skills from "@/components/Skills";
import Projects from "@/components/Projects";
import Certifications from "@/components/Certifications";
import Education from "@/components/Education";
import Contact from "@/components/Contact";

export default function Home() {
  return (
    <main className="flex-grow">
      <Hero />
      <About />
      <Skills />
      <Projects />
      <Certifications />
      <Education />
      <Contact />
    </main>
  );
}
