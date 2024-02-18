import React, { useState, useEffect } from 'react';

const TrialVisualization = ({ deviceDescription, useIndication}) => {
    // State to store the iframe URL
    const [iframeUrl, setIframeUrl] = useState('');

    // Fetch the URL from the Flask endpoint when the component mounts
    useEffect(() => {
        const fetchIframeUrl = async () => {
            try {
                const response = await fetch('/api/visualize-trials', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    // Convert your object to a URL-encoded string
                    body: new URLSearchParams({
                        'device-description': deviceDescription,
                        'use-indication': useIndication
                    })
                });
                const data = await response.json();
                if (data.url) {
                    setIframeUrl(data.url);
                }
            } catch (error) {
                console.error('Failed to fetch iframe URL:', error);
            }
        };

        fetchIframeUrl();
    }, []); // Dependencies could include variables like deviceDescription and useIndication if they are dynamic

    // CSS for centering the iframe
    const iframeStyle = {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh', // Adjust the height as needed
        width: '100%' // Adjust the width as needed
    };

    return (
        <section className="container mx-auto antialiased bg-gray-100 text-gray-600 min-h-screen p-4">
            <h1 className="font-semibold text-gray-800 text-2xl text-center">Visualizing Similar Clinical Trials</h1>
            <div style={{height: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                {iframeUrl && <iframe src={iframeUrl} title="Trial Visualization" style={{width: '80%', height: '80%', border: 'none'}} />}
            </div>
        </section>
    );
};

export default TrialVisualization;