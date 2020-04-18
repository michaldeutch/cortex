import { Container, Row, Col, Card, CardBody } from "shards-react";

import PageTitle from "../components/common/PageTitle";
import React, { useState, useEffect } from 'react';


function Tables() {
  const [users, setAllUsers] = useState(0);

  useEffect(() => {
    let local_users = [];
    fetch('/users').then(res => res.json()).then(data => {
    for (let i=0; i<data.length; i++) {
      let user = data[i];
      local_users.push(
        <tr key={i}>
          <td>{i + 1}</td>
          <td>{user['username']}</td>
          <td>{user['user_id']}</td>
        </tr>
      );
    }
    setAllUsers(local_users);
  });
  }, []);


  return (
    <Container fluid className="main-content-container px-4">
      <Row noGutters className="page-header py-4">
        <PageTitle sm="4" title="Users" subtitle="details"
                   className="text-sm-left"/>
      </Row>
      <Row>
        <Col>
          <Card small className="mb-4 overflow-hidden">
            <CardBody className="bg-dark p-0 pb-3">
              <table className="table table-dark mb-0">
                <thead className="thead-dark">
                <tr>
                  <th scope="col" className="border-0">
                    #
                  </th>
                  <th scope="col" className="border-0">
                    Name
                  </th>
                  <th scope="col" className="border-0">
                    ID
                  </th>
                </tr>
                </thead>
                <tbody>{users}</tbody>
              </table>
            </CardBody>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default Tables;
