import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const downloadInspectionReport = async (inspectionId: string) => {
    try {
        const response = await axios.get(
            `${API_BASE_URL}/inspection/report/${inspectionId}`,
            { responseType: 'blob' }
        );
        
        // Create blob link to download
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `inspection_report_${inspectionId}.pdf`);
        
        // Append to html link element page
        document.body.appendChild(link);
        
        // Start download
        link.click();
        
        // Clean up and remove the link
        link.parentNode?.removeChild(link);
    } catch (error) {
        console.error('Error downloading inspection report:', error);
        throw error;
    }
};

export const downloadMonthlyReport = async (year: number, month: number) => {
    try {
        const response = await axios.get(
            `${API_BASE_URL}/inspection/monthly-report/${year}/${month}`,
            { responseType: 'blob' }
        );
        
        // Create blob link to download
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `monthly_report_${year}_${month}.pdf`);
        
        // Append to html link element page
        document.body.appendChild(link);
        
        // Start download
        link.click();
        
        // Clean up and remove the link
        link.parentNode?.removeChild(link);
    } catch (error) {
        console.error('Error downloading monthly report:', error);
        throw error;
    }
}; 