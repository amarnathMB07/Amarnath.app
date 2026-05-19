"use client";
import { motion } from "framer-motion";
import { Code, Database, Award, BookOpen } from "lucide-react";

export default function About() {
  const stats = [
    { icon: <Code size={24} />, title: "Projects Completed", value: "10+" },
    { icon: <Award size={24} />, title: "Certifications", value: "5+" },
    { icon: <Database size={24} />, title: "Technologies", value: "15+" },
    { icon: <BookOpen size={24} />, title: "Education", value: "Final Year" },
  ];

  return (
    <section id="about" className="py-24 relative">
      <div className="container mx-auto px-6">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold mb-4">About <span className="text-gradient">Me</span></h2>
          <div className="w-24 h-1 bg-primary mx-auto rounded-full" />
        </motion.div>

        <div className="flex flex-col lg:flex-row gap-16 items-center">
          <motion.div 
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="flex-1 space-y-6 text-lg text-slate-600 dark:text-slate-400"
          >
            <p>
              Hello! I'm Amarnath MB, a final year student with a deep passion for <strong className="text-slate-900 dark:text-slate-200">Full-Stack Development, Data Analytics, and AI</strong>. 
            </p>
            <p>
              My journey in tech started with a curiosity to understand how things work under the hood. Since then, I've immersed myself in learning modern web technologies like the MERN stack and Next.js, while simultaneously exploring the powerful world of Data Science with Python, SQL, and Power BI.
            </p>
            <p>
              I thrive on problem-solving and turning complex ideas into elegant, user-friendly digital solutions. Whether it's building a responsive web app or analyzing datasets to extract actionable insights, I am always eager to learn, adapt, and create impact.
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="flex-1 grid grid-cols-2 gap-6 w-full"
          >
            {stats.map((stat, index) => (
              <div key={index} className="glass p-6 rounded-2xl flex flex-col items-center justify-center text-center transform hover:-translate-y-2 transition-transform duration-300">
                <div className="text-primary mb-4 p-4 rounded-full bg-primary/10">
                  {stat.icon}
                </div>
                <h4 className="text-3xl font-bold text-slate-800 dark:text-slate-100 mb-2">{stat.value}</h4>
                <p className="text-sm text-slate-500 dark:text-slate-400 font-medium">{stat.title}</p>
              </div>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  );
}
