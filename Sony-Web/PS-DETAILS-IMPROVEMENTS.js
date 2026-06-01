/**
 * MEJORAS A AGREGAR EN PS-Details.html
 * Integración de timestamps y badges en las notas técnicas
 */

// Función auxiliar para formatear fecha/hora
function formatNoteTimestamp(isoString) {
  if (!isoString) return '';
  const date = new Date(isoString);
  const now = new Date();
  const diff = now - date;
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor(diff / (1000 * 60));
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));

  if (minutes < 1) return 'Hace unos segundos';
  if (minutes < 60) return `Hace ${minutes} min`;
  if (hours < 24) return `Hace ${hours}h`;
  if (days === 1) return 'Ayer';
  if (days < 7) return `Hace ${days} días`;
  
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

// Función para crear badge de "NUEVA NOTA"
function createNewNoteBadge() {
  return `<span class="note-new-badge" title="Nota recién actualizada">✨ NUEVA</span>`;
}

// REEMPLAZO DE CÓDIGO EN PS-Details.html línea ~630-668
// El código mejorado sería:

/*
technicalNotes.forEach((tn, idx) => {
  const uniqueId = `note-${idx}`;
  const isNew = tn.timestamp && (new Date() - new Date(tn.timestamp)) < 86400000; // menos de 24h
  const timeStr = formatNoteTimestamp(tn.timestamp);
  
  gridHtml += `
    <div class="note-card" data-note-id="${uniqueId}">
      <div class="note-card-header">
        <div class="note-card-title">
          <i class="fa-regular fa-rectangle-list"></i> ${escapeHtml(tn.title || 'Nota técnica')}
          ${tn.badge ? `<span class="note-badge">${escapeHtml(tn.badge)}</span>` : ''}
          ${isNew ? createNewNoteBadge() : ''}
        </div>
        <div class="note-toggle-icon"><i class="fa-solid fa-chevron-down"></i></div>
      </div>
      <div class="note-card-body" id="${uniqueId}">
        <div class="note-timestamp" style="font-size: 0.75rem; color: var(--muted); margin-bottom: 0.8rem;">
          <i class="fa-regular fa-calendar"></i> ${timeStr || 'Fecha desconocida'}
        </div>
        <div class="note-author"><i class="fa-regular fa-user"></i> ${escapeHtml(tn.author || 'Fuente oficial')}</div>
        <div class="note-info">${escapeHtml(tn.info || 'Sin información adicional.')}</div>
        <div class="note-meta">
          ${tn.link ? `<a href="${escapeHtml(tn.link)}" target="_blank" rel="noopener" class="note-link"><i class="fa-solid fa-arrow-up-right-from-m"></i> Documentación</a>` : ''}
          ${tn.backport ? `<span class="backport-tag"><i class="fa-solid fa-undo-alt"></i> ${escapeHtml(tn.backport)}</span>` : ''}
          ${tn.noteId ? `<span class="backport-tag" style="background:var(--pill);"><i class="fa-regular fa-id-card"></i> ${escapeHtml(tn.noteId)}</span>` : ''}
          ${tn.version ? `<span class="backport-tag" style="background: rgba(20, 184, 166, 0.1); border: 1px solid rgba(20, 184, 166, 0.3);"><i class="fa-solid fa-code-branch"></i> v${escapeHtml(tn.version)}</span>` : ''}
        </div>
      </div>
    </div>
  `;
});
*/

// CSS A AGREGAR EN PS-Details.html para los nuevos estilos:

/*
.note-new-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  background: linear-gradient(135deg, #14b8a6 0%, #06b6d4 100%);
  color: white;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  margin-left: 0.5rem;
  animation: badgePulse 2s ease-in-out infinite;
}

@keyframes badgePulse {
  0%, 100% { box-shadow: 0 0 8px rgba(20, 184, 166, 0.3); }
  50% { box-shadow: 0 0 16px rgba(20, 184, 166, 0.6); }
}

.note-timestamp {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem;
  background: var(--note-highlight);
  border-radius: 8px;
  font-size: 0.75rem;
  color: var(--muted);
}

.note-card-body {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.4s cubic-bezier(0.22, 0.61, 0.36, 1), opacity 0.3s ease;
  opacity: 0;
}

.note-card-body.open {
  max-height: 500px;
  opacity: 1;
  padding: 1.2rem;
}
*/
