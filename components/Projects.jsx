"use client";
import { motion } from "framer-motion";
import { Github, ExternalLink } from "lucide-react";
import Link from "next/link";

export default function Projects() {
  const projects = [
    {
      title: "AgroSmart - Crop Monitoring",
      description: "A smart crop monitoring and assistance platform providing real-time data insights, weather forecasts, and AI-driven crop recommendations.",
      image: "https://images.unsplash.com/photo-1628102491629-778571d893a3?q=80&w=800&auto=format&fit=crop",
      tags: ["React.js", "Node.js", "MongoDB", "Python", "IoT"],
      github: "https://github.com",
      demo: "https://example.com"
    },
    {
      title: "E-Commerce Analytics Dashboard",
      description: "A comprehensive dashboard for visualizing e-commerce sales data, user behavior, and revenue trends with interactive charts.",
      image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=800&auto=format&fit=crop",
      tags: ["Power BI", "SQL", "Excel", "Pandas"],
      github: "https://github.com",
      demo: "https://example.com"
    },
    {
      title: "IoT Smart Monitoring System",
      description: "Hardware and software integrated solution for monitoring environmental factors like temperature, humidity, and soil moisture in real-time.",
      image: "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=800&auto=format&fit=crop",
      tags: ["C++", "Python", "React.js", "Express"],
      github: "https://github.com",
      demo: "https://example.com"
    },
    {
      title: "Modern Portfolio Website",
      description: "This very website! A highly interactive, dark-themed developer portfolio built with Next.js, Tailwind CSS, and Framer Motion.",
      image: "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?q=80&w=800&auto=format&fit=crop",
      tags: ["Next.js", "Tailwind CSS", "Framer Motion"],
      github: "https://github.com/amarnathMB07/Amarnath.app",
      demo: "https://amarnath-app.vercel.app"
    }
  ];

  return (
    <section id="projects" className="py-24 relative">
      <div className="container mx-auto px-6">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold mb-4">Featured <span className="text-gradient">Projects</span></h2>
          <div className="w-24 h-1 bg-primary mx-auto rounded-full" />
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
          {projects.map((project, index) => (
            <motion.div 
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="glass rounded-2xl overflow-hidden group hover:shadow-[0_0_30px_rgba(59,130,246,0.2)] transition-shadow duration-300 flex flex-col border border-slate-200 dark:border-white/10"
            >
              <div className="relative h-64 overflow-hidden">
                <img 
                  src={project.image} 
                  alt={project.title} 
                  className="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700"
                />
                <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center gap-4">
                  <Link href={project.github} target="_blank" className="p-3 bg-white text-slate-900 rounded-full hover:bg-primary hover:text-white transition-colors transform hover:scale-110">
                    <Github size={20} />
                  </Link>
                  <Link href={project.demo} target="_blank" className="p-3 bg-white text-slate-900 rounded-full hover:bg-primary hover:text-white transition-colors transform hover:scale-110">
                    <ExternalLink size={20} />
                  </Link>
                </div>
              </div>
              <div className="p-8 flex-grow flex flex-col bg-white dark:bg-transparent">
                <h3 className="text-2xl font-bold mb-3 text-slate-800 dark:text-slate-100 group-hover:text-primary transition-colors">{project.title}</h3>
                <p className="text-slate-600 dark:text-slate-400 mb-6 flex-grow">{project.description}</p>
                <div className="flex flex-wrap gap-2 mt-auto">
                  {project.tags.map((tag, tagIndex) => (
                    <span key={tagIndex} className="text-xs font-semibold px-3 py-1 bg-primary/10 text-primary rounded-full">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
