import { FaroRouteTracker } from '@grafana/faro-react';
import { initializeFaro } from '@grafana/faro-web-sdk';
import { TracingInstrumentation } from '@grafana/faro-web-tracing';

// Initialize Faro
const faro = initializeFaro({
  url: 'http://localhost:12347/collect',
  app: {
    name: 'faro-react-app',
    version: '1.0.0'
  },
  plugins: [
    new TracingInstrumentation()
  ]
});

function App() {
  return (
    <div className="App">
      <FaroRouteTracker>
        <h1>Faro React App</h1>
        {/* Your app content */}
      </FaroRouteTracker>
    </div>
  );
}

export default App;
