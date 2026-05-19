"use client";
import { Github, Linkedin, Mail, Instagram } from "lucide-react";
import Link from "next/link";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-slate-200 dark:border-white/10 py-12 relative overflow-hidden">
       {/* Background gradient subtle */}
       <div className="absolute inset-0 bg-gradient-to-b from-transparent to-primary/5 dark:to-primary/10 pointer-events-none" />
       
      <div className="container mx-auto px-6 relative z-10 flex flex-col items-center">
        <h2 className="text-2xl font-bold mb-6 text-gradient">Amarnath MB</h2>
        
        <div className="flex items-center space-x-6 mb-8">
          <Link href="https://github.com/amarnathMB07" target="_blank" className="p-3 rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-primary hover:text-white dark:hover:bg-primary transition-all duration-300 transform hover:-translate-y-1">
            <Github size={20} />
          </Link>
          <Link href="https://www.linkedin.com/in/amarnath-mb-754b6340b" target="_blank" className="p-3 rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-primary hover:text-white dark:hover:bg-primary transition-all duration-300 transform hover:-translate-y-1">
            <Linkedin size={20} />
          </Link>
          <Link href="mailto:a36933811@gmail.com" className="p-3 rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-primary hover:text-white dark:hover:bg-primary transition-all duration-300 transform hover:-translate-y-1">
            <Mail size={20} />
          </Link>
          <Link href="https://instagram.com" target="_blank" className="p-3 rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-primary hover:text-white dark:hover:bg-primary transition-all duration-300 transform hover:-translate-y-1">
            <Instagram size={20} />
          </Link>
        </div>

        <p className="text-slate-500 dark:text-slate-400 text-sm">
          &copy; {currentYear} Amarnath MB. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
