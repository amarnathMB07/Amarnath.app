"use client";
import { motion } from "framer-motion";
import { Award, Calendar } from "lucide-react";

export default function Certifications() {
  const certs = [
    { title: "Cloud Computing (Elite Grade)", organization: "NPTEL", date: "Recent" },
    { title: "Paper Presentation", organization: "SRM College", date: "Recent" },
    { title: "Technical Workshop", organization: "VIT College", date: "Recent" },
    { title: "Data Analytics Certification", organization: "Google / Coursera", date: "2023" },
    { title: "Python for Data Science", organization: "IBM", date: "2023" },
    { title: "Power BI Workshop", organization: "Microsoft", date: "2022" },
    { title: "Web Development Bootcamp", organization: "Udemy", date: "2021" },
  ];

  return (
    <section id="certifications" className="py-24 relative bg-slate-50 dark:bg-slate-900/50">
      <div className="container mx-auto px-6">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold mb-4">Licenses & <span className="text-gradient">Certifications</span></h2>
          <div className="w-24 h-1 bg-primary mx-auto rounded-full" />
        </motion.div>

        <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
          {certs.map((cert, index) => (
            <motion.div 
              key={index}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="glass p-6 rounded-2xl border border-slate-200 dark:border-white/10 flex items-start gap-4 hover:-translate-y-1 transition-transform duration-300 bg-white dark:bg-transparent"
            >
              <div className="p-3 bg-primary/10 text-primary rounded-xl">
                <Award size={24} />
              </div>
              <div>
                <h3 className="text-xl font-bold text-slate-800 dark:text-slate-100 mb-1">{cert.title}</h3>
                <p className="text-slate-600 dark:text-slate-400 font-medium">{cert.organization}</p>
                <div className="flex items-center text-sm text-slate-500 mt-2 gap-1">
                  <Calendar size={14} />
                  <span>{cert.date}</span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
