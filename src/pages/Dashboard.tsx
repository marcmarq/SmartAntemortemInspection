import React from 'react'
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import ReportActions from '../components/ReportActions'

interface InspectionSummary {
  total: number
  completed: number
  inProgress: number
  detections: number
}

const Dashboard: React.FC = () => {
  const [summary, setSummary] = useState<InspectionSummary>({
    total: 0,
    completed: 0,
    inProgress: 0,
    detections: 0,
  })

  useEffect(() => {
    // TODO: Fetch actual data from the API
    setSummary({
      total: 150,
      completed: 120,
      inProgress: 30,
      detections: 45,
    })
  }, [])

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
      
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-2xl font-semibold mb-4">Reports</h2>
        <p className="text-gray-600 mb-4">
          Download inspection reports and monthly summaries
        </p>
        <ReportActions />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="rounded-lg border bg-card text-card-foreground shadow-sm p-6">
          <div className="flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="text-sm font-medium">Total Inspections</h3>
          </div>
          <div className="text-2xl font-bold">{summary.total}</div>
        </div>

        <div className="rounded-lg border bg-card text-card-foreground shadow-sm p-6">
          <div className="flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="text-sm font-medium">Completed</h3>
          </div>
          <div className="text-2xl font-bold">{summary.completed}</div>
        </div>

        <div className="rounded-lg border bg-card text-card-foreground shadow-sm p-6">
          <div className="flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="text-sm font-medium">In Progress</h3>
          </div>
          <div className="text-2xl font-bold">{summary.inProgress}</div>
        </div>

        <div className="rounded-lg border bg-card text-card-foreground shadow-sm p-6">
          <div className="flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="text-sm font-medium">Total Detections</h3>
          </div>
          <div className="text-2xl font-bold">{summary.detections}</div>
        </div>
      </div>

      <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
        <div className="p-6">
          <h3 className="text-lg font-medium">Recent Inspections</h3>
        </div>
        <div className="p-6 pt-0">
          <div className="relative w-full overflow-auto">
            <table className="w-full caption-bottom text-sm">
              <thead className="[&_tr]:border-b">
                <tr className="border-b transition-colors hover:bg-muted/50">
                  <th className="h-10 px-2 text-left align-middle font-medium">
                    ID
                  </th>
                  <th className="h-10 px-2 text-left align-middle font-medium">
                    Date
                  </th>
                  <th className="h-10 px-2 text-left align-middle font-medium">
                    Status
                  </th>
                  <th className="h-10 px-2 text-left align-middle font-medium">
                    Detections
                  </th>
                </tr>
              </thead>
              <tbody className="[&_tr:last-child]:border-0">
                <tr className="border-b transition-colors hover:bg-muted/50">
                  <td className="p-2 align-middle">#12345</td>
                  <td className="p-2 align-middle">2023-11-25</td>
                  <td className="p-2 align-middle">
                    <span className="inline-flex items-center rounded-md bg-green-50 px-2 py-1 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20">
                      Completed
                    </span>
                  </td>
                  <td className="p-2 align-middle">3</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard 