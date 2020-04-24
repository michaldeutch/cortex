import React, { useState, useEffect } from 'react';
import PropTypes from "prop-types";
import {
  Container,
  Row,
  Col,
  CardImgOverlay,
  Card,
  CardImg,
  CardTitle,
} from "shards-react";

import PageTitle from "./../components/common/PageTitle";
import SmallStats from "./../components/common/SmallStats";
import Snapshot from "../components/common/Snapshot";

function Overview({ smallStats }) {
  const [user, setUser] = useState(0);
  const [snapshots, setSnapshots] = useState([]);
  const [genderImg, setGenderImg] = useState(require("../images/Gender.svg"));
  const [birthday, setBirthday] = useState("No Birthday");
  const [allSnapshots, setAllSnapshots] = useState(0);

  let stats = smallStats[0];
  useEffect(() => {
    fetch(window.location.pathname).then(res => res.json()).then(data => {
      setUser(data);
      if ("gender" in data) {
        if (data["gender"] === 0)
          setGenderImg(require("../images/Male.svg"));
        else if (data["gender"] === 1)
          setGenderImg(require("../images/Female.svg"));
      }
      if ("birthday" in data) {
        setBirthday(data["birthday"]);
      }
    });
  }, []);

  useEffect(() => {
    fetch(window.location.pathname + "/snapshots")
      .then(res => res.json()).then(data => {
      let sortedSnapshots = data.sort((s1, s2) => s1["datetime"] <= s2["datetime"]);
      setSnapshots(sortedSnapshots);
      let allSnaps = [];
      let lastSnap;
      sortedSnapshots.forEach((snapshot, ind) => {
        if (ind % 2 === 0) {
          lastSnap = <Snapshot
            key = {ind}
            snapshot={snapshot}
            ind = {ind}
          />;
        }
        else{
          allSnaps.push(<Row key={ind}>
            {lastSnap}
            <Snapshot
              key = {ind}
              snapshot={snapshot}
              ind = {ind}
            />
          </Row>)
        }
      });
      setAllSnapshots(allSnaps);
  });
  }, []);


  return (
  <Container fluid className="main-content-container px-4">
    {/* Page Header */}
    <Row noGutters className="page-header py-4">
      <PageTitle title={user["username"]} subtitle="Overview" className="text-sm-left mb-3" />
    </Row>

    <Row>

        <Col className="col-lg mb-4" key={1} {...stats.attrs}>
          <Card small className="stats-small">
              <CardImg variant="middle" src={genderImg} alt="Card image cap" style={{ maxWidth: "150px", maxHeight: "120px", alignSelf: 'center' }}>
              </CardImg>
          </Card>
        </Col>

        <Col className="col-lg mb-4 text-center" key={2} {...stats.attrs}>
          <Card small className="stats-small">
            <CardImg variant="middle" src={require("../images/Birthday.svg")} alt="Card image cap" style={{ maxWidth: "150px", maxHeight: "120px", alignSelf: 'center', opacity: 0.7 }}>
            </CardImg>
            <CardImgOverlay>
              <CardTitle>
                {birthday}
              </CardTitle>
            </CardImgOverlay>
          </Card>
        </Col>

    </Row>

    <Row>
        <Col className="col-lg mb-4" key={0} {...stats.attrs}>
          <SmallStats
            id={`small-stats-${0}`}
            variation="1"
            chartData={stats.datasets}
            chartLabels={stats.chartLabels}
            label={stats.label}
            value={snapshots.length}
            percentage={0}
            increase={false}
            decrease={false}
          />
        </Col>
    </Row>
    {allSnapshots}
  </Container>
);
}

Overview.propTypes = {
  /**
   * The small stats dataset.
   */
  smallStats: PropTypes.array
};

Overview.defaultProps = {
  smallStats: [
    {
      label: "Snapshots",
      value: "0",
      percentage: "0%",
      increase: true,
      chartLabels: [],
      attrs: { md: "6", sm: "6" },
      datasets: [
        {
          label: "Today",
          fill: "start",
          borderWidth: 1.5,
          backgroundColor: "rgba(23,198,113,0.1)",
          borderColor: "rgb(23,198,113)",
          data: [1, 2, 3, 3, 3, 4, 4]
        }
      ]
    }
  ]
};

export default Overview;
