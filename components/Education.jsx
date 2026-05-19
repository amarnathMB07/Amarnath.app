"use client";
import { motion } from "framer-motion";
import { GraduationCap, Calendar } from "lucide-react";

export default function Education() {
  const education = [
    {
      degree: "B.Tech in Artificial Intelligence and Data Science",
      institution: "Dhanalakshmi Srinivasan Engineering College (Perambalur)",
      duration: "2023 - 2027 (Final Year)",
      description: "Focusing on Full Stack Development, Data Structures, Algorithms, and Data Analytics. Maintaining a strong academic record.",
      courses: ["Data Structures", "DBMS", "Web Development", "Artificial Intelligence"]
    },
    {
      degree: "Higher Secondary Education (12th Standard)",
      institution: "Light Land HSS",
      duration: "2020 - 2022",
      description: "Completed with 75.08% marks. Major subjects: Physics, Chemistry, Mathematics, and Computer Science.",
      courses: []
    },
    {
      degree: "Secondary School Education (10th Standard)",
      institution: "Model HSS",
      duration: "Completed",
      description: "Completed with 96% marks.",
      courses: []
    }
  ];

  return (
    <section id="education" className="py-24 relative">
      <div className="container mx-auto px-6">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold mb-4">My <span className="text-gradient">Education</span></h2>
          <div className="w-24 h-1 bg-primary mx-auto rounded-full" />
        </motion.div>

        <div className="max-w-3xl mx-auto relative">
          {/* Timeline Line */}
          <div className="absolute left-0 md:left-1/2 transform md:-translate-x-1/2 top-0 bottom-0 w-1 bg-slate-200 dark:bg-slate-800 rounded-full" />

          {education.map((item, index) => (
            <div key={index} className={`relative mb-12 flex flex-col md:flex-row items-center ${index % 2 === 0 ? 'md:flex-row-reverse' : ''}`}>
              {/* Timeline Dot */}
              <div className="absolute left-[-8px] md:left-1/2 transform md:-translate-x-1/2 w-5 h-5 bg-primary rounded-full border-4 border-white dark:border-slate-900 z-10" />

              <motion.div 
                initial={{ opacity: 0, x: index % 2 === 0 ? 50 : -50 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6 }}
                className={`ml-8 md:ml-0 md:w-1/2 ${index % 2 === 0 ? 'md:pl-12' : 'md:pr-12'}`}
              >
                <div className="glass p-8 rounded-2xl border border-slate-200 dark:border-white/10 hover:shadow-lg transition-shadow duration-300 relative overflow-hidden group bg-white dark:bg-transparent">
                  <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity transform group-hover:scale-110">
                    <GraduationCap size={80} />
                  </div>
                  
                  <h3 className="text-2xl font-bold text-slate-800 dark:text-slate-100 mb-2">{item.degree}</h3>
                  <p className="text-primary font-semibold text-lg mb-2">{item.institution}</p>
                  <div className="flex items-center text-slate-500 mb-4 gap-2">
                    <Calendar size={16} />
                    <span className="text-sm font-medium">{item.duration}</span>
                  </div>
                  <p className="text-slate-600 dark:text-slate-400 mb-4 leading-relaxed">
                    {item.description}
                  </p>
                  
                  {item.courses.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {item.courses.map((course, i) => (
                        <span key={i} className="text-xs font-semibold px-2 py-1 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 rounded">
                          {course}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </motion.div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
