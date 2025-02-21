import { Faro } from '@grafana/faro-web-sdk';
import { FaroRouteTracker } from '@grafana/faro-react';

const faro = new Faro({
  url: 'http://localhost:4318/v1/metrics',
  app: {
    name: 'faro-react-app',
    version: '1.0.0'
  },
  instrumentations: []
});

export default function App() {
  return (
    <div>
      <FaroRouteTracker />
      <h1>Faro Monitoring Demo</h1>
    </div>
  );
}
