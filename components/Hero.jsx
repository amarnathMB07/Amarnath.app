"use client";
import { motion } from "framer-motion";
import { Download, ArrowRight, Mail } from "lucide-react";
import Link from "next/link";

export default function Hero() {
  return (
    <section id="hero" className="min-h-screen flex items-center justify-center pt-20 relative overflow-hidden">
      {/* Background gradients */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-[120px] pointer-events-none" />

      <div className="container mx-auto px-6 relative z-10 flex flex-col md:flex-row items-center justify-between gap-12">
        <motion.div 
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8 }}
          className="flex-1 text-center md:text-left"
        >
          <h2 className="text-xl md:text-2xl font-medium text-slate-600 dark:text-slate-300 mb-4">
            Hi, I'm
          </h2>
          <h1 className="text-5xl md:text-7xl font-bold mb-6 tracking-tight">
            Amarnath <span className="text-gradient">MB</span>
          </h1>
          <h3 className="text-2xl md:text-3xl font-semibold text-slate-700 dark:text-slate-200 mb-8">
            Full Stack Developer & Data Analyst Student
          </h3>
          <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto md:mx-0 mb-10 leading-relaxed">
            I craft responsive websites and analyze complex data. Final year student passionate about building scalable web applications, generating data insights, and solving real-world problems through code.
          </p>
          
          <div className="flex flex-wrap items-center justify-center md:justify-start gap-4">
            <Link href="#projects" className="px-8 py-4 bg-primary text-white rounded-full font-medium flex items-center gap-2 hover:bg-blue-600 transition-all shadow-[0_0_20px_rgba(59,130,246,0.4)] hover:shadow-[0_0_30px_rgba(59,130,246,0.6)] transform hover:-translate-y-1">
              View Projects <ArrowRight size={18} />
            </Link>
            <Link href="https://drive.google.com/file/d/1uHUXpfRmEENIOKIxm6jyIORawRDZ24Gz/view?usp=drivesdk" target="_blank" className="px-8 py-4 bg-slate-800 text-white dark:bg-white dark:text-slate-900 rounded-full font-medium flex items-center gap-2 hover:bg-slate-700 dark:hover:bg-slate-100 transition-all shadow-lg transform hover:-translate-y-1">
              View Resume <Download size={18} />
            </Link>
            <Link href="#contact" className="p-4 rounded-full border border-slate-300 dark:border-slate-700 hover:border-primary dark:hover:border-primary hover:text-primary dark:hover:text-primary transition-all bg-transparent backdrop-blur-sm">
              <Mail size={20} />
            </Link>
          </div>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="flex-1 flex justify-center md:justify-end"
        >
          <div className="relative w-72 h-72 md:w-[400px] md:h-[400px]">
            {/* Glowing border effect */}
            <div className="absolute inset-0 rounded-full bg-gradient-to-tr from-primary to-purple-500 blur-2xl opacity-50 animate-pulse" />
            <div className="absolute inset-2 rounded-full glass border-4 border-white/10 overflow-hidden flex items-center justify-center bg-slate-200 dark:bg-slate-800 shadow-2xl">
              <span className="text-6xl font-bold text-slate-400 dark:text-slate-600">AMB</span>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
