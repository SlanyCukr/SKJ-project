import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';
import * as serviceWorker from './serviceWorker';
import App from './App';
import { ApolloClient, InMemoryCache, ApolloProvider } from '@apollo/client';

var config = require('./config.json');

const client = new ApolloClient({
  uri: localStorage.getItem('urlGraphQL') || "http://" + config.graphql_server_host + ":" + config.graphql_server_port + "/graphql",
  cache: new InMemoryCache()
});

ReactDOM.render((
  <ApolloProvider client={client}>
  <BrowserRouter>
    <App />
  </BrowserRouter>
  </ApolloProvider>
), document.getElementById('root'));

serviceWorker.unregister();
