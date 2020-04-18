import React, { useState, useEffect } from 'react';
import { Redirect } from "react-router-dom";

// Layout Types
import { DefaultLayout } from "./layouts";

// Route Views
import Tables from "./views/Tables";


export default
[
  {
    path: "/",
    exact: true,
    layout: DefaultLayout,
    component: () => <Redirect to="/tables" />
  },
  {
    path: "/tables",
    layout: DefaultLayout,
    component: Tables
  }
];
