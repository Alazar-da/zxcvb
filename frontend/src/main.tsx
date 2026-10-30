import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Area, AreaChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import './styles.css';

const API = import.meta.env.API_URL || 'http://localhost:8000';
type Point = { start_time: string; generation_mw: number; publish_time?: string };
type Forecast = { delivery_date: string; decision_cutoff: string; points: Point[]; actuals: Point[] };
type Metrics = { count:number; mae_mw:number; rmse_mw:number; normalized_error_pct:number; mean_bias_mw:number; p90_abs_error_mw:number; p95_abs_error_mw:number };

function App() {
  const [date, setDate] = useState('2026-01-15');
  const [forecast, setForecast] = useState<Forecast | null>(null);
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  useEffect(() => { fetch(`${API}/api/forecast?delivery_date=${date}`).then(r => r.json()).then(setForecast); fetch(`${API}/api/accuracy`).then(r => r.json()).then(setMetrics); }, [date]);
  const data = forecast?.points.map((p, i) => ({ time: new Date(p.start_time).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'}), forecast: p.generation_mw, actual: forecast.actuals[i]?.generation_mw })) || [];
  return <main>
    <header><div><span className="eyebrow">NORTHSTAR ENERGY · TRADING DESK</span><h1>Wind procurement intelligence</h1><p>Decision-time forecasts for GB day-ahead power buying.</p></div><div className="status"><span/> DEMO SNAPSHOT</div></header>
    <section className="control card"><label>Delivery date <input type="date" min="2026-01-01" max="2026-01-31" value={date} onChange={e=>setDate(e.target.value)}/></label><div className="cutoff"><small>DECISION CUTOFF</small><strong>D-1 · 11:00 Europe/London</strong><span>Forecast vintage available at auction gate closure</span></div></section>
    <section className="grid">
      <div className="card chart-card"><div className="section-head"><div><span className="eyebrow">FEATURE 01 · AS-OF DECISION</span><h2>Forecast vs actual generation</h2></div><span className="pill">48 settlement periods</span></div><div className="chart"><ResponsiveContainer width="100%" height="100%"><AreaChart data={data}><defs><linearGradient id="wind" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#65d6c4" stopOpacity={.45}/><stop offset="95%" stopColor="#65d6c4" stopOpacity={0}/></linearGradient></defs><CartesianGrid strokeDasharray="3 3" stroke="#23434b"/><XAxis dataKey="time" tick={{fill:'#8da6aa',fontSize:11}} interval={7}/><YAxis tick={{fill:'#8da6aa',fontSize:11}}/><Tooltip/><Legend/><Area type="monotone" dataKey="forecast" name="Decision-time forecast" stroke="#65d6c4" fill="url(#wind)"/><Area type="monotone" dataKey="actual" name="Actual generation" stroke="#f4b86a" fill="none"/></AreaChart></ResponsiveContainer></div><div className="meta">Vintage used: {forecast?.points[0] ? new Date(forecast.points[0].publish_time!).toLocaleString() : '—'} · Cutoff applied: {forecast ? new Date(forecast.decision_cutoff).toLocaleString() : '—'}</div></div>
      <aside className="card"><span className="eyebrow">FEATURE 02 · ACCURACY</span><h2>Procurement margin signal</h2>{metrics && <><div className="metric"><small>MAE</small><b>{metrics.mae_mw.toFixed(0)} <em>MW</em></b></div><div className="metric"><small>P90 ABS ERROR</small><b>{metrics.p90_abs_error_mw.toFixed(0)} <em>MW</em></b></div><div className="metric"><small>MEAN BIAS</small><b className={metrics.mean_bias_mw >= 0 ? 'positive':''}>{metrics.mean_bias_mw.toFixed(0)} <em>MW</em></b></div><p className="takeaway">Across {metrics.count.toLocaleString()} half-hours, forecasts underestimated actual wind by <strong>{metrics.mean_bias_mw.toFixed(0)} MW</strong> on average. Use the P90 error as a practical safety-margin input.</p></>}</aside>
    </section>
    <footer>Source: Elexon BMRS · Scope: GB national wind · Data mode is clearly labelled for demo use</footer>
  </main>
}
createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>);

