import React, { useEffect, useState } from 'react'
import Plot from 'react-plotly.js'

function Metrics({ data }) {
  if (!data || data.length === 0) return null
  const n = data.length
  const mae = (arr) => arr.reduce((s, v) => s + Math.abs(v.predicted - v.actual), 0) / arr.length
  const mse = (arr) => arr.reduce((s, v) => s + Math.pow(v.predicted - v.actual, 2), 0) / arr.length
  const rmse = Math.sqrt(mse(data))
  const r2 = () => null
  return (
    <div className="metrics">
      <div>Samples: {n}</div>
      <div>MAE: {mae(data).toFixed(2)}</div>
      <div>RMSE: {rmse.toFixed(2)}</div>
    </div>
  )
}

function PredictionsTable({ data }) {
  if (!data) return null

  // Simple table render (removed dependency on react-table hooks)
  return (
    <table className="pred-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Actual</th>
          <th>Predicted</th>
        </tr>
      </thead>
      <tbody>
        {data.map((row, i) => (
          <tr key={i}>
            <td>{row.id}</td>
            <td>{row.actual}</td>
            <td>{row.predicted}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

export default function App() {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch('/predictions.json')
      .then((r) => r.json())
      .then((j) => setData(j))
      .catch((e) => console.error('Failed to load predictions.json', e))
  }, [])

  return (
    <div className="container">
      <h1>Credit Risk — Model Results</h1>
      <Metrics data={data} />

      <div className="plot">
        {data && (
          <Plot
            data={[
              {
                x: data.map((d) => d.actual),
                y: data.map((d) => d.predicted),
                mode: 'markers',
                type: 'scatter',
                marker: { color: 'blue' }
              },
              {
                x: [Math.min(...data.map((d) => d.actual)), Math.max(...data.map((d) => d.actual))],
                y: [Math.min(...data.map((d) => d.actual)), Math.max(...data.map((d) => d.actual))],
                mode: 'lines',
                line: { dash: 'dash', color: 'red' },
                name: 'Identity'
              }
            ]}
            layout={{ width: 700, height: 500, title: 'Actual vs Predicted' }}
          />
        )}
      </div>

      <h2>Predictions Table</h2>
      <PredictionsTable data={data} />
    </div>
  )
}
