"use client";
import { motion } from "framer-motion";

export default function Skills() {
  const technicalSkills = [
    { name: "HTML/CSS", level: 90 },
    { name: "JavaScript", level: 85 },
    { name: "React.js", level: 80 },
    { name: "Next.js", level: 75 },
    { name: "Node.js & Express.js", level: 70 },
    { name: "MongoDB", level: 75 },
    { name: "Python", level: 85 },
    { name: "SQL", level: 80 },
  ];

  const dataSkills = [
    { name: "Power BI", level: 85 },
    { name: "Excel", level: 90 },
    { name: "Pandas", level: 80 },
    { name: "Data Analytics", level: 85 },
  ];

  const otherSkills = [
    "Git & GitHub", "REST APIs", "Tailwind CSS", "Framer Motion", "Problem Solving", "AI Integration"
  ];

  const SkillBar = ({ name, level }) => (
    <div className="mb-6">
      <div className="flex justify-between items-center mb-2">
        <span className="font-medium text-slate-700 dark:text-slate-300">{name}</span>
        <span className="text-sm text-slate-500">{level}%</span>
      </div>
      <div className="h-3 w-full bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
        <motion.div 
          initial={{ width: 0 }}
          whileInView={{ width: `${level}%` }}
          viewport={{ once: true }}
          transition={{ duration: 1, ease: "easeOut" }}
          className="h-full bg-gradient-to-r from-primary to-purple-500 rounded-full relative"
        >
          {/* Animated shine effect */}
          <motion.div 
            animate={{ x: ["-100%", "200%"] }}
            transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
            className="absolute top-0 left-0 h-full w-1/3 bg-gradient-to-r from-transparent via-white/30 to-transparent skew-x-12"
          />
        </motion.div>
      </div>
    </div>
  );

  return (
    <section id="skills" className="py-24 relative bg-slate-50 dark:bg-slate-900/50">
      <div className="container mx-auto px-6">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold mb-4">My <span className="text-gradient">Skills</span></h2>
          <div className="w-24 h-1 bg-primary mx-auto rounded-full" />
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-16">
          <motion.div 
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <h3 className="text-2xl font-bold mb-8 text-slate-800 dark:text-slate-100 flex items-center gap-2">
              <span className="text-primary">{'< />'}</span> Full Stack Development
            </h3>
            <div className="glass p-8 rounded-2xl">
              {technicalSkills.map((skill, index) => (
                <SkillBar key={index} {...skill} />
              ))}
            </div>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <h3 className="text-2xl font-bold mb-8 text-slate-800 dark:text-slate-100 flex items-center gap-2">
              <span className="text-primary">📊</span> Data Analytics
            </h3>
            <div className="glass p-8 rounded-2xl mb-8">
              {dataSkills.map((skill, index) => (
                <SkillBar key={index} {...skill} />
              ))}
            </div>

            <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-slate-100">Other Skills & Tools</h3>
            <div className="flex flex-wrap gap-3">
              {otherSkills.map((skill, index) => (
                <span key={index} className="px-4 py-2 bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-full text-sm font-medium hover:bg-primary hover:text-white dark:hover:bg-primary transition-colors cursor-default border border-transparent hover:border-primary/50">
                  {skill}
                </span>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
