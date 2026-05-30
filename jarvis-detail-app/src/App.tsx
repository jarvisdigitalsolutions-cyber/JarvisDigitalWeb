import React from "react";
import { motion } from "framer-motion";
import { Check, ChevronLeft, Crown, Gamepad2, Globe, Monitor, Play, Settings, Share2, Sparkles, Star, Trophy } from "lucide-react";

const chips = ["Acción", "Sigilo", "Espionaje", "Aventura", "Tiro táctico"];

const features = [
  "Misiones de infiltración",
  "Uso de gadgets y herramientas de espionaje",
  "Combate táctico y sigiloso",
  "Estilo cinematográfico de agente secreto",
  "Origen reimaginado de James Bond",
];

export default function JarvisGameDetailPage() {
  return (
    <div className="min-h-screen bg-[#040816] text-white">

      {/* HEADER */}
      <header className="border-b border-white/10 bg-[#050b1a]/70 backdrop-blur-xl">
        <div className="mx-auto flex max-w-[1600px] items-center justify-between px-6 py-4">
          <div className="flex items-center gap-4">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-cyan-400/30 bg-cyan-400/10">
              <Sparkles className="h-5 w-5 text-cyan-300" />
            </div>
            <div>
              <div className="tracking-[0.3em]">JARVIS</div>
              <div className="text-xs text-cyan-300">Digital Solutions</div>
            </div>
          </div>

          <nav className="hidden md:flex gap-6 text-sm text-slate-300">
            <a href="#">Catálogo</a>
            <a href="#">Inicio</a>
            <a href="#">Registro</a>
            <a className="text-white border-b border-cyan-400" href="#">Detalle</a>
          </nav>

          <div className="flex gap-2">
            <button className="w-10 h-10 rounded-full bg-white/10"><Settings size={18} /></button>
            <button className="w-10 h-10 rounded-full bg-white/10 text-sm font-semibold">CU</button>
            <button className="px-4 py-2 rounded-full bg-white/10 flex items-center gap-2 text-sm">
              <ChevronLeft size={16}/> Volver
            </button>
          </div>
        </div>
      </header>

      {/* LAYOUT */}
      <main className="mx-auto max-w-[1600px] px-6 py-10 grid grid-cols-[260px_1fr_320px] gap-8">

        {/* COVER FUERA DEL BLOQUE */}
        <aside className="sticky top-10">
          <div className="rounded-[24px] overflow-hidden border border-cyan-400/20 shadow-lg">
            <img
              src="https://images.unsplash.com/photo-1606112219348-204d7d8b94ee?w=300&h=450&fit=crop"
              alt="007 First Light"
              className="w-full h-[420px] object-cover"
            />
          </div>
        </aside>

        {/* CONTENIDO CENTRAL */}
        <section className="space-y-6">

          <h1 className="text-5xl font-bold">007 First Light</h1>

          <div className="flex gap-3 flex-wrap">
            {chips.map(c => (
              <span key={c} className="px-4 py-2 bg-white/5 rounded-full text-sm border border-white/10">{c}</span>
            ))}
          </div>

          {/* TRAILER GRANDE FULL WIDTH */}
          <div className="rounded-[30px] overflow-hidden border border-cyan-400/20 bg-[#0b1222]">

            <div className="flex justify-between items-center px-6 py-4 border-b border-white/10">
              <div className="flex items-center gap-3">
                <Play size={20} />
                <span>Tráiler Oficial</span>
              </div>
              <Share2 size={20} />
            </div>

            {/* VIDEO MÁS GRANDE */}
            <div className="relative w-full h-[520px]">
              <img
                src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1000&h=600&fit=crop"
                alt="Trailer"
                className="w-full h-full object-cover"
              />

              <div className="absolute inset-0 flex items-center justify-center">
                <button className="w-24 h-24 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center hover:bg-white/30 transition">
                  <Play size={40} className="ml-1"/>
                </button>
              </div>
            </div>
          </div>

          {/* DESCRIPCIÓN BIEN ALINEADA */}
          <div className="grid grid-cols-2 gap-6">

            <div className="bg-white/5 p-6 rounded-2xl border border-white/10">
              <h2 className="text-xl mb-3 font-semibold">Descripción</h2>
              <p className="text-slate-300 leading-relaxed text-sm">
                Una aventura de espionaje con infiltración, gadgets y combate táctico.
                Estilo cinematográfico con acción fluida y elegante. Historia de origen reimaginada.
              </p>

              {/* ICONOS ORDENADOS */}
              <div className="grid grid-cols-4 gap-4 mt-6 text-center">
                <Mini icon={Globe} text="Online" />
                <Mini icon={Gamepad2} text="Control" />
                <Mini icon={Monitor} text="Cloud" />
                <Mini icon={Trophy} text="Logros" />
              </div>
            </div>

            <div className="bg-white/5 p-6 rounded-2xl border border-white/10">
              <h2 className="text-xl font-semibold mb-4">Especificaciones</h2>
              <div className="space-y-3">
                <Row label="Plataforma" value="PS5" />
                <Row label="Edición" value="Digital" />
                <Row label="Desarrollador" value="IO Interactive" />
                <Row label="Calificación" value="4.7/5" />
              </div>
            </div>

          </div>

        </section>

        {/* DERECHA */}
        <aside>
          <div className="bg-white/5 p-6 rounded-2xl border border-white/10">
            <div className="flex items-center gap-2 mb-4">
              <h2 className="text-lg font-semibold">Mecánicas</h2>
              <Crown size={18} className="text-cyan-300" />
            </div>
            {features.map(f => (
              <div key={f} className="flex justify-between items-start py-3 border-b border-white/10 gap-2">
                <span className="text-sm text-slate-200">{f}</span>
                <Check className="text-cyan-400 flex-shrink-0" size={18} />
              </div>
            ))}
          </div>
        </aside>

      </main>
    </div>
  );
}

function Mini({ icon: Icon, text }: { icon: any; text: string }) {
  return (
    <div>
      <Icon className="mx-auto mb-2" size={20} />
      <div className="text-xs text-slate-300">{text}</div>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between border-b border-white/10 pb-2">
      <span className="text-slate-400 text-sm">{label}</span>
      <span className="text-sm font-medium">{value}</span>
    </div>
  );
}
