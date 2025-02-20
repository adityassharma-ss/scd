// package.json
{
  "name": "faro-react-demo",
  "version": "0.1.0",
  "dependencies": {
    "@grafana/faro-react": "^1.3.5",
    "@grafana/faro-web-sdk": "^1.3.5",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  }
}

// src/faro-setup.js
import { getWebInstrumentations, initializeFaro } from '@grafana/faro-web-sdk';
import { TracingInstrumentation } from '@grafana/faro-web-tracing';
import { ReactIntegration } from '@grafana/faro-react';

export const initializeFaroMonitoring = () => {
  initializeFaro({
    url: 'YOUR_FARO_COLLECTOR_URL', // Replace with your Faro collector URL
    app: {
      name: 'Faro React Demo',
      version: '1.0.0',
      environment: 'production'
    },
    instrumentations: [
      ...getWebInstrumentations(),
      new TracingInstrumentation(),
      new ReactIntegration(),
    ],
    // Optional: Configure additional settings
    sessionTracking: {
      enabled: true,
    },
    isolatedErrors: {
      enabled: true,
    }
  });
};

// src/App.jsx
import React, { useEffect } from 'react';
import { initializeFaroMonitoring } from './faro-setup';

function App() {
  useEffect(() => {
    initializeFaroMonitoring();
  }, []);

  // Example button to generate errors for testing
  const generateError = () => {
    throw new Error('Test error for Faro monitoring');
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Faro React Demo</h1>
      <button 
        className="bg-blue-500 text-white px-4 py-2 rounded"
        onClick={generateError}
      >
        Generate Test Error
      </button>
    </div>
  );
}

export default App;
