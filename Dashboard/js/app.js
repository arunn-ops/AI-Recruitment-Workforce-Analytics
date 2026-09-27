// Main Dashboard Application JavaScript
let chartInstances = {};

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initDatabaseStatus();
  loadAllDashboardData();
  initPredictorForm();
  initSearchAndFilters();
});

// Navigation Handling
function initNavigation() {
  const navItems = document.querySelectorAll('.nav-item');
  const sections = document.querySelectorAll('.tab-section');
  const pageTitle = document.getElementById('pageTitle');

  navItems.forEach(item => {
    item.addEventListener('click', () => {
      const targetTab = item.getAttribute('data-tab');
      
      navItems.forEach(n => n.classList.remove('active'));
      sections.forEach(s => s.classList.remove('active'));

      item.classList.add('active');
      document.getElementById(`tab-${targetTab}`).classList.add('active');
      pageTitle.innerText = item.getAttribute('data-title') || 'Dashboard';
    });
  });
}

// Database Status Indicator
async function initDatabaseStatus() {
  try {
    const res = await fetch('/api/status');
    const data = await res.json();
    const statusText = document.getElementById('dbStatusText');
    if (data.connected) {
      statusText.innerHTML = `DB Connected: <strong>${data.source}</strong> (${data.total_records} records)`;
    } else {
      statusText.innerHTML = `<span style="color: var(--danger)">Connection Error</span>`;
    }
  } catch (e) {
    document.getElementById('dbStatusText').innerText = 'Offline Mode (Local API Server)';
  }
}

// Global Filter Setup
function initSearchAndFilters() {
  const deptFilter = document.getElementById('deptFilter');
  const searchInput = document.getElementById('searchInput');

  // Populate Department Filter options
  fetch('/api/department')
    .then(r => r.json())
    .then(data => {
      if (data.metrics) {
        data.metrics.forEach(d => {
          const opt = document.createElement('option');
          opt.value = d.Department_Name;
          opt.innerText = d.Department_Name;
          deptFilter.appendChild(opt);
        });
      }
    });

  deptFilter.addEventListener('change', filterHiringSummary);
  searchInput.addEventListener('input', debounce(filterHiringSummary, 300));
}

function debounce(func, wait) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

// Fetch and Load Data across all Tabs
async function loadAllDashboardData() {
  loadOverview();
  loadRecruitment();
  loadDepartment();
  loadRecruiter();
  loadCandidate();
  loadScores();
  loadSalary();
  loadMLMetrics();
  filterHiringSummary();
}

// 1. OVERVIEW TAB
async function loadOverview() {
  const res = await fetch('/api/overview');
  const data = await res.json();

  document.getElementById('kpi-tot-candidates').innerText = Number(data.total_candidates || 0).toLocaleString();
  document.getElementById('kpi-tot-apps').innerText = Number(data.total_applications || 0).toLocaleString();
  document.getElementById('kpi-tot-hired').innerText = Number(data.total_hired || 0).toLocaleString();
  document.getElementById('kpi-hiring-rate').innerText = `${data.hiring_rate}%`;
  document.getElementById('kpi-avg-score').innerText = `${data.avg_overall_score} / 100`;
  document.getElementById('kpi-avg-exp-sal').innerText = `₹${(data.avg_expected_salary / 100000).toFixed(2)} L`;
  document.getElementById('kpi-avg-off-sal').innerText = `₹${(data.avg_offered_salary / 100000).toFixed(2)} L`;

  // Overview Funnel Chart
  destroyChart('chart-overview-funnel');
  const funnelCtx = document.getElementById('chart-overview-funnel').getContext('2d');
  chartInstances['chart-overview-funnel'] = ChartFactory.createBarChart(
    funnelCtx,
    ['Applied', 'Interviewed', 'Offered', 'Hired', 'Rejected'],
    [data.total_applications, data.total_interviewed, data.total_offered, data.total_hired, data.total_rejected],
    'Candidate Funnel Volume'
  );
}

// 2. RECRUITMENT ANALYTICS TAB
async function loadRecruitment() {
  const res = await fetch('/api/recruitment');
  const data = await res.json();

  // Status Doughnut
  destroyChart('chart-rec-status');
  const statusCtx = document.getElementById('chart-rec-status').getContext('2d');
  chartInstances['chart-rec-status'] = ChartFactory.createDoughnutChart(
    statusCtx,
    data.status_breakdown.map(s => s.Status),
    data.status_breakdown.map(s => s.count)
  );

  // Source Conversion Bar
  destroyChart('chart-rec-source');
  const sourceCtx = document.getElementById('chart-rec-source').getContext('2d');
  chartInstances['chart-rec-source'] = ChartFactory.createBarChart(
    sourceCtx,
    data.source_breakdown.map(s => s.Recruitment_Source),
    data.source_breakdown.map(s => s.conversion_rate),
    'Conversion Rate (%)',
    true
  );

  // Job Role Applications
  destroyChart('chart-rec-roles');
  const roleCtx = document.getElementById('chart-rec-roles').getContext('2d');
  chartInstances['chart-rec-roles'] = ChartFactory.createBarChart(
    roleCtx,
    data.job_roles.slice(0, 8).map(r => r.Job_Role),
    data.job_roles.slice(0, 8).map(r => r.count),
    'Applications Volume'
  );

  // Monthly Trend Line
  destroyChart('chart-rec-trend');
  const trendCtx = document.getElementById('chart-rec-trend').getContext('2d');
  chartInstances['chart-rec-trend'] = ChartFactory.createLineChart(
    trendCtx,
    data.monthly_trends.map(t => t.month_year),
    [
      { label: 'Applications', data: data.monthly_trends.map(t => t.total_apps) },
      { label: 'Hires', data: data.monthly_trends.map(t => t.hires) }
    ]
  );
}

// 3. DEPARTMENT ANALYTICS TAB
async function loadDepartment() {
  const res = await fetch('/api/department');
  const data = await res.json();

  // Dept Applications & Hires Grouped Bar
  destroyChart('chart-dept-apps');
  const deptCtx = document.getElementById('chart-dept-apps').getContext('2d');
  chartInstances['chart-dept-apps'] = ChartFactory.createGroupedBarChart(
    deptCtx,
    data.metrics.map(d => d.Department_Name),
    [
      { label: 'Total Applications', data: data.metrics.map(d => d.Total_Applications) },
      { label: 'Hires Count', data: data.metrics.map(d => d.Hired_Count) }
    ]
  );

  // Render Department Metrics Table
  const tbody = document.getElementById('tbody-dept-metrics');
  tbody.innerHTML = '';
  data.metrics.forEach(d => {
    tbody.innerHTML += `
      <tr>
        <td><strong>${d.Department_Name}</strong></td>
        <td>${d.Total_Applications}</td>
        <td>${d.Hired_Count}</td>
        <td><span class="badge badge-hired">${d.Dept_Hiring_Rate_Percent}%</span></td>
        <td>${d.Avg_Candidate_Age} yrs</td>
        <td>${d.Avg_Notice_Period_Days} days</td>
      </tr>
    `;
  });
}

// 4. RECRUITER PERFORMANCE TAB
async function loadRecruiter() {
  const res = await fetch('/api/recruiter');
  const data = await res.json();

  const metrics = data.recruiter_metrics;

  destroyChart('chart-recruiter-perf');
  const recCtx = document.getElementById('chart-recruiter-perf').getContext('2d');
  chartInstances['chart-recruiter-perf'] = ChartFactory.createGroupedBarChart(
    recCtx,
    metrics.map(r => r.Recruiter_Name),
    [
      { label: 'Managed Applications', data: metrics.map(r => r.Total_Applications_Managed) },
      { label: 'Hires Completed', data: metrics.map(r => r.Total_Hired) }
    ]
  );

  const tbody = document.getElementById('tbody-recruiter-metrics');
  tbody.innerHTML = '';
  metrics.forEach(r => {
    tbody.innerHTML += `
      <tr>
        <td><strong>${r.Recruiter_Name}</strong></td>
        <td>${r.Total_Applications_Managed}</td>
        <td>${r.Total_Interviewed}</td>
        <td>${r.Total_Offered}</td>
        <td>${r.Total_Hired}</td>
        <td><span class="badge badge-hired">${r.Recruiter_Hiring_Rate_Percent}%</span></td>
        <td>${r.Avg_Overall_Score_Of_Candidates}</td>
      </tr>
    `;
  });
}

// 5. CANDIDATE ANALYTICS TAB
async function loadCandidate() {
  const res = await fetch('/api/candidate');
  const data = await res.json();

  // Education Doughnut
  destroyChart('chart-cand-edu');
  const eduCtx = document.getElementById('chart-cand-edu').getContext('2d');
  chartInstances['chart-cand-edu'] = ChartFactory.createDoughnutChart(
    eduCtx,
    data.education.map(e => e.Education),
    data.education.map(e => e.count)
  );

  // Location Bar
  destroyChart('chart-cand-loc');
  const locCtx = document.getElementById('chart-cand-loc').getContext('2d');
  chartInstances['chart-cand-loc'] = ChartFactory.createBarChart(
    locCtx,
    data.location.slice(0, 10).map(l => l.Location),
    data.location.slice(0, 10).map(l => l.count),
    'Candidates Count',
    true
  );

  // Experience Distribution Bar
  destroyChart('chart-cand-exp');
  const expCtx = document.getElementById('chart-cand-exp').getContext('2d');
  chartInstances['chart-cand-exp'] = ChartFactory.createBarChart(
    expCtx,
    data.experience.map(e => `${e.Experience} Yrs`),
    data.experience.map(e => e.count),
    'Experience Volume'
  );
}

// 6. SCORE ANALYSIS TAB
async function loadScores() {
  const res = await fetch('/api/scores');
  const data = await res.json();

  // Scores by Status Radar
  destroyChart('chart-scores-status');
  const statusCtx = document.getElementById('chart-scores-status').getContext('2d');
  chartInstances['chart-scores-status'] = ChartFactory.createRadarChart(
    statusCtx,
    ['Resume ATS', 'Technical', 'HR', 'Communication', 'Overall'],
    data.by_status.map(s => ({
      label: s.Status,
      data: [s.avg_ats, s.avg_tech, s.avg_hr, s.avg_comm, s.avg_overall]
    }))
  );

  // Scores by Department Grouped Bar
  destroyChart('chart-scores-dept');
  const deptCtx = document.getElementById('chart-scores-dept').getContext('2d');
  chartInstances['chart-scores-dept'] = ChartFactory.createGroupedBarChart(
    deptCtx,
    data.by_dept.map(d => d.Department_Name),
    [
      { label: 'ATS Score', data: data.by_dept.map(d => d.avg_ats) },
      { label: 'Tech Score', data: data.by_dept.map(d => d.avg_tech) },
      { label: 'HR Score', data: data.by_dept.map(d => d.avg_hr) },
      { label: 'Overall', data: data.by_dept.map(d => d.avg_overall) }
    ]
  );
}

// 7. SALARY ANALYSIS TAB
async function loadSalary() {
  const res = await fetch('/api/salary');
  const data = await res.json();

  // Salary by Dept
  destroyChart('chart-salary-dept');
  const deptCtx = document.getElementById('chart-salary-dept').getContext('2d');
  chartInstances['chart-salary-dept'] = ChartFactory.createGroupedBarChart(
    deptCtx,
    data.by_dept.map(d => d.Department_Name),
    [
      { label: 'Avg Expected CTC (₹)', data: data.by_dept.map(d => d.avg_expected) },
      { label: 'Avg Offered CTC (₹)', data: data.by_dept.map(d => d.avg_offered) }
    ]
  );

  // Salary by Job Role
  destroyChart('chart-salary-role');
  const roleCtx = document.getElementById('chart-salary-role').getContext('2d');
  chartInstances['chart-salary-role'] = ChartFactory.createBarChart(
    roleCtx,
    data.by_role.slice(0, 8).map(r => r.Job_Role),
    data.by_role.slice(0, 8).map(r => r.avg_expected),
    'Avg Expected CTC (₹)',
    true
  );
}

// 8. ML ANALYTICS TAB
async function loadMLMetrics() {
  const res = await fetch('/api/ml-metrics');
  const data = await res.json();

  document.getElementById('ml-accuracy').innerText = `${data.accuracy}%`;
  document.getElementById('ml-samples').innerText = `${data.train_samples} Train / ${data.test_samples} Test`;

  // Feature Importance Bar
  destroyChart('chart-ml-features');
  const featCtx = document.getElementById('chart-ml-features').getContext('2d');
  chartInstances['chart-ml-features'] = ChartFactory.createBarChart(
    featCtx,
    data.top_features.map(f => f.feature),
    data.top_features.map(f => (f.importance * 100).toFixed(2)),
    'Importance Weight (%)',
    true
  );

  // Confusion Matrix Grid
  const cm = data.confusion_matrix || [[0, 0], [0, 0]];
  document.getElementById('cm-tn').innerText = cm[0][0];
  document.getElementById('cm-fp').innerText = cm[0][1];
  document.getElementById('cm-fn').innerText = cm[1][0];
  document.getElementById('cm-tp').innerText = cm[1][1];
}

// Predictor Form Submission
function initPredictorForm() {
  const form = document.getElementById('predictorForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      ats_score: document.getElementById('pred-ats').value,
      tech_score: document.getElementById('pred-tech').value,
      hr_score: document.getElementById('pred-hr').value,
      comm_score: document.getElementById('pred-comm').value
    };

    try {
      const res = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const result = await res.json();

      document.getElementById('pred-prob').innerText = `${result.selection_probability}%`;
      const resLabel = document.getElementById('pred-outcome');
      resLabel.innerText = result.predicted_result;
      resLabel.style.color = result.predicted_result === 'Selected' ? 'var(--success)' : 'var(--danger)';
      document.getElementById('pred-overall-calc').innerText = `Calculated Overall Score: ${result.overall_score} / 100`;
    } catch (e) {
      alert('Error running prediction model');
    }
  });
}

// 9. DATA EXPLORER TAB (FILTERABLE TABLE)
async function filterHiringSummary() {
  const dept = document.getElementById('deptFilter').value;
  const search = document.getElementById('searchInput').value;

  const url = `/api/hiring-summary?dept=${encodeURIComponent(dept)}&search=${encodeURIComponent(search)}`;
  const res = await fetch(url);
  const data = await res.json();

  const tbody = document.getElementById('tbody-hiring-summary');
  tbody.innerHTML = '';
  document.getElementById('table-count-badge').innerText = `${data.length} Candidates`;

  data.forEach(c => {
    const statusClass = `badge-${(c.Status || 'Applied').toLowerCase()}`;
    tbody.innerHTML += `
      <tr>
        <td><code>${c.Candidate_ID}</code></td>
        <td><strong>${c.Candidate_Name}</strong></td>
        <td>${c.Department_Name || '-'}</td>
        <td>${c.Job_Role || '-'}</td>
        <td>${c.Candidate_Location || '-'}</td>
        <td>${c.Overall_Score}</td>
        <td>₹${(c.Expected_Salary / 100000).toFixed(2)} L</td>
        <td><span class="badge ${statusClass}">${c.Status}</span></td>
        <td>${c.Recruiter_Name || '-'}</td>
        <td>${c.Result}</td>
      </tr>
    `;
  });
}

function destroyChart(id) {
  if (chartInstances[id]) {
    chartInstances[id].destroy();
    delete chartInstances[id];
  }
}
