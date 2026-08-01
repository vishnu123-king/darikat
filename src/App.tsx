import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { CareerObjective } from './components/CareerObjective';
import { SkillsSection } from './components/SkillsSection';
import { ProjectsSection } from './components/ProjectsSection';
import { CertificationsSection } from './components/CertificationsSection';
import { EducationSection } from './components/EducationSection';
import { ContactSection } from './components/ContactSection';
import { Footer } from './components/Footer';
import { ResumeModal } from './components/ResumeModal';

export default function App() {
  const [isResumeModalOpen, setIsResumeModalOpen] = useState(false);

  useEffect(() => {
    // Process HTMX dynamically generated nodes if needed
    if (window.htmx) {
      window.htmx.process(document.body);
    }
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-emerald-500 selection:text-slate-950">
      
      {/* Navigation Header */}
      <Navbar onOpenResume={() => setIsResumeModalOpen(true)} />

      {/* Main Content Area */}
      <main className="flex-1">
        <Hero onOpenResume={() => setIsResumeModalOpen(true)} />
        <CareerObjective />
        <SkillsSection />
        <ProjectsSection />
        <CertificationsSection />
        <EducationSection />
        <ContactSection />
      </main>

      {/* Footer */}
      <Footer />

      {/* Printable / Full Resume Modal */}
      <ResumeModal 
        isOpen={isResumeModalOpen} 
        onClose={() => setIsResumeModalOpen(false)} 
      />

    </div>
  );
}

declare global {
  interface Window {
    htmx?: {
      process: (element: HTMLElement) => void;
    };
  }
}
