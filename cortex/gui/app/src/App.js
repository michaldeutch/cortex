import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";

import routes from "./routes";
import withTracker from "./withTracker";

import "bootstrap/dist/css/bootstrap.min.css";
import "./shards-dashboard/styles/shards-dashboards.1.1.0.min.css";
import {DefaultLayout} from "./layouts";
import BlogOverview from "./views/BlogOverview";

function App() {
  const [allRoutes, setAllRoutes] = useState(0);

  useEffect(() => {
    let local = routes.map(route => route);
    fetch('/users').then(res => res.json()).then(data => {
      for (let i=0; i<data.length; i++) {
        let user = data[i];
        local.push(
          {
            path: "/users/" + user['user_id'],
            layout: DefaultLayout,
            component: BlogOverview
          }
        );
      }

      local = local.map((route, index) => {
        return (
          <Route
            key={index}
            path={route.path}
            exact={route.exact}
            component={withTracker(props => {
              return (
                <route.layout {...props}>
                  <route.component {...props} />
                </route.layout>
              );
            })}
          />
        );
      });
      setAllRoutes(local);
    });
  }, []);

  return (
    <Router basename={process.env.REACT_APP_BASENAME || ""}>
      <div>
        {allRoutes}
      </div>
    </Router>
  );
}

export default App;
