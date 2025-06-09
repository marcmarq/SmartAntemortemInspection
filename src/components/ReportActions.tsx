import React, { useState } from 'react';
import { downloadInspectionReport, downloadMonthlyReport } from '../services/api';

interface ReportActionsProps {
    inspectionId?: string;
}

const ReportActions: React.FC<ReportActionsProps> = ({ inspectionId }) => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleDownloadInspection = async () => {
        if (!inspectionId) return;
        
        setIsLoading(true);
        setError(null);
        try {
            await downloadInspectionReport(inspectionId);
        } catch (err) {
            setError('Failed to download inspection report');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleDownloadMonthly = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const now = new Date();
            await downloadMonthlyReport(now.getFullYear(), now.getMonth() + 1);
        } catch (err) {
            setError('Failed to download monthly report');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col gap-4 p-4">
            {inspectionId && (
                <button
                    onClick={handleDownloadInspection}
                    disabled={isLoading}
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
                >
                    {isLoading ? 'Downloading...' : 'Download Inspection Report'}
                </button>
            )}
            
            <button
                onClick={handleDownloadMonthly}
                disabled={isLoading}
                className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
            >
                {isLoading ? 'Downloading...' : 'Download Monthly Report'}
            </button>

            {error && (
                <div className="text-red-500 text-sm mt-2">
                    {error}
                </div>
            )}
        </div>
    );
};

export default ReportActions; 