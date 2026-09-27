// Chart.js Default Dark Theme Configuration
Chart.defaults.color = '#94A3B8';
Chart.defaults.font.family = "'Segoe UI', sans-serif";
Chart.defaults.font.size = 12;

const PALETTE = [
  '#0EA5E9', // Cyan
  '#3B82F6', // Blue
  '#10B981', // Emerald Green
  '#EF4444', // Red
  '#F59E0B', // Amber
  '#8B5CF6', // Purple
  '#EC4899', // Pink
  '#64748B'  // Slate
];

const ChartFactory = {
  createBarChart(ctx, labels, data, title, isHorizontal = false) {
    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: title,
          data: data,
          backgroundColor: PALETTE[0],
          borderRadius: 6,
          hoverBackgroundColor: '#0284C7'
        }]
      },
      options: {
        indexAxis: isHorizontal ? 'y' : 'x',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#0F172A',
            titleColor: '#F8FAFC',
            bodyColor: '#94A3B8',
            borderColor: '#334155',
            borderWidth: 1
          }
        },
        scales: {
          x: { grid: { color: 'rgba(255,255,255,0.05)' } },
          y: { grid: { color: 'rgba(255,255,255,0.05)' } }
        }
      }
    });
  },

  createGroupedBarChart(ctx, labels, datasets) {
    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: datasets.map((ds, idx) => ({
          label: ds.label,
          data: ds.data,
          backgroundColor: PALETTE[idx % PALETTE.length],
          borderRadius: 4
        }))
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#F8FAFC' } },
          tooltip: {
            backgroundColor: '#0F172A',
            titleColor: '#F8FAFC',
            bodyColor: '#94A3B8',
            borderColor: '#334155',
            borderWidth: 1
          }
        },
        scales: {
          x: { grid: { color: 'rgba(255,255,255,0.05)' } },
          y: { grid: { color: 'rgba(255,255,255,0.05)' } }
        }
      }
    });
  },

  createDoughnutChart(ctx, labels, data) {
    return new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: PALETTE.slice(0, labels.length),
          borderWidth: 2,
          borderColor: '#1E293B'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { color: '#F8FAFC', padding: 15 } },
          tooltip: {
            backgroundColor: '#0F172A',
            borderColor: '#334155',
            borderWidth: 1
          }
        },
        cutout: '70%'
      }
    });
  },

  createLineChart(ctx, labels, datasets) {
    return new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: datasets.map((ds, idx) => ({
          label: ds.label,
          data: ds.data,
          borderColor: PALETTE[idx % PALETTE.length],
          backgroundColor: PALETTE[idx % PALETTE.length] + '20',
          fill: true,
          tension: 0.35,
          pointRadius: 4,
          pointHoverRadius: 6
        }))
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#F8FAFC' } },
          tooltip: {
            backgroundColor: '#0F172A',
            borderColor: '#334155',
            borderWidth: 1
          }
        },
        scales: {
          x: { grid: { color: 'rgba(255,255,255,0.05)' } },
          y: { grid: { color: 'rgba(255,255,255,0.05)' } }
        }
      }
    });
  },

  createRadarChart(ctx, labels, datasets) {
    return new Chart(ctx, {
      type: 'radar',
      data: {
        labels: labels,
        datasets: datasets.map((ds, idx) => ({
          label: ds.label,
          data: ds.data,
          borderColor: PALETTE[idx % PALETTE.length],
          backgroundColor: PALETTE[idx % PALETTE.length] + '33',
          borderWidth: 2
        }))
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#F8FAFC' } }
        },
        scales: {
          r: {
            angleLines: { color: 'rgba(255,255,255,0.1)' },
            grid: { color: 'rgba(255,255,255,0.1)' },
            pointLabels: { color: '#F8FAFC', font: { size: 11 } },
            ticks: { backdropColor: 'transparent', color: '#94A3B8' }
          }
        }
      }
    });
  }
};
