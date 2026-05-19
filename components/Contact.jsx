"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { Send, MapPin, Phone, Mail } from "lucide-react";

export default function Contact() {
  const [formData, setFormData] = useState({ name: "", email: "", message: "" });
  const [status, setStatus] = useState("idle"); // idle, submitting, success, error

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus("submitting");

    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (res.ok) {
        setStatus("success");
        setFormData({ name: "", email: "", message: "" });
        setTimeout(() => setStatus("idle"), 5000);
      } else {
        setStatus("error");
        setTimeout(() => setStatus("idle"), 5000);
      }
    } catch (error) {
      setStatus("error");
      setTimeout(() => setStatus("idle"), 5000);
    }
  };

  return (
    <section id="contact" className="py-24 relative bg-slate-50 dark:bg-slate-900/50">
      <div className="container mx-auto px-6">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold mb-4">Get In <span className="text-gradient">Touch</span></h2>
          <div className="w-24 h-1 bg-primary mx-auto rounded-full" />
          <p className="mt-6 text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            Whether you have a question, a project idea, or just want to say hi, feel free to drop a message!
          </p>
        </motion.div>

        <div className="max-w-5xl mx-auto flex flex-col md:flex-row gap-12">
          {/* Contact Info */}
          <motion.div 
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="flex-1 space-y-8"
          >
            <div className="flex items-start gap-4">
              <div className="p-4 bg-primary/10 text-primary rounded-xl">
                <Mail size={24} />
              </div>
              <div>
                <h4 className="text-xl font-bold text-slate-800 dark:text-slate-100 mb-1">Email</h4>
                <p className="text-slate-600 dark:text-slate-400">a36933811@gmail.com</p>
              </div>
            </div>
            
            <div className="flex items-start gap-4">
              <div className="p-4 bg-primary/10 text-primary rounded-xl">
                <MapPin size={24} />
              </div>
              <div>
                <h4 className="text-xl font-bold text-slate-800 dark:text-slate-100 mb-1">Location</h4>
                <p className="text-slate-600 dark:text-slate-400">Kollam, Kerala, India</p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="p-4 bg-primary/10 text-primary rounded-xl">
                <Phone size={24} />
              </div>
              <div>
                <h4 className="text-xl font-bold text-slate-800 dark:text-slate-100 mb-1">Phone</h4>
                <p className="text-slate-600 dark:text-slate-400">+91 97785 52209</p>
              </div>
            </div>
          </motion.div>

          {/* Contact Form */}
          <motion.div 
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="flex-[1.5]"
          >
            <form onSubmit={handleSubmit} className="glass p-8 rounded-2xl flex flex-col gap-6 bg-white dark:bg-transparent">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="flex flex-col gap-2">
                  <label htmlFor="name" className="text-sm font-medium text-slate-700 dark:text-slate-300">Name</label>
                  <input 
                    type="text" 
                    id="name" 
                    name="name" 
                    required
                    value={formData.name}
                    onChange={handleChange}
                    className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-white/10 focus:outline-none focus:border-primary transition-colors text-slate-900 dark:text-slate-100"
                    placeholder="John Doe"
                  />
                </div>
                <div className="flex flex-col gap-2">
                  <label htmlFor="email" className="text-sm font-medium text-slate-700 dark:text-slate-300">Email</label>
                  <input 
                    type="email" 
                    id="email" 
                    name="email" 
                    required
                    value={formData.email}
                    onChange={handleChange}
                    className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-white/10 focus:outline-none focus:border-primary transition-colors text-slate-900 dark:text-slate-100"
                    placeholder="john@example.com"
                  />
                </div>
              </div>
              <div className="flex flex-col gap-2">
                <label htmlFor="message" className="text-sm font-medium text-slate-700 dark:text-slate-300">Message</label>
                <textarea 
                  id="message" 
                  name="message" 
                  rows="5"
                  required
                  value={formData.message}
                  onChange={handleChange}
                  className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-white/10 focus:outline-none focus:border-primary transition-colors text-slate-900 dark:text-slate-100 resize-none"
                  placeholder="Your message here..."
                ></textarea>
              </div>
              
              <button 
                type="submit" 
                disabled={status === "submitting"}
                className="py-3 px-6 bg-primary text-white rounded-lg font-medium flex items-center justify-center gap-2 hover:bg-blue-600 transition-all disabled:opacity-70 disabled:cursor-not-allowed"
              >
                {status === "submitting" ? "Sending..." : "Send Message"} 
                <Send size={18} />
              </button>

              {status === "success" && (
                <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-green-500 text-center font-medium">Message sent successfully!</motion.p>
              )}
              {status === "error" && (
                <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-red-500 text-center font-medium">Something went wrong. Please try again.</motion.p>
              )}
            </form>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
