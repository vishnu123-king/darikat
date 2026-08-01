export interface Skill {
  name: string;
  category: 'programming' | 'tools' | 'soft';
  level: string;
  desc: string;
  icon: string;
  color: string;
}

export interface Project {
  id: string;
  title: string;
  subtitle: string;
  tech: string[];
  description: string[];
  category: 'python' | 'sql' | 'ai' | 'excel';
  badge: string;
}

export interface Certification {
  title: string;
  issuer: string;
  date: string;
  skills: string[];
  icon: string;
}

export interface Education {
  degree: string;
  period: string;
  institution: string;
  location?: string;
}
