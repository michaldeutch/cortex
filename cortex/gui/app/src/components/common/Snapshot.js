import React from "react";
import {
  Collapse,
  Col, Card, CardBody, CardImg, CardTitle, CardText, Button
} from "shards-react";
import Tabs from 'react-bootstrap/Tabs';
import Tab from "react-bootstrap/Tab";
import {Bar} from 'react-chartjs-2';

export default class Snapshot extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      visible: false,
      feelings: {
                  labels: ['Hunger', 'Thirst', 'Exhaustion',
                           'Happiness'],
                  datasets: [
                    {
                      backgroundColor: 'rgba(0,0,255,1)',
                      borderColor: 'rgba(0,0,0,1)',
                      borderWidth: 1,
                      data: [0, 0, 0, 0]
                    }
                  ]
                },
      pose: "disabled",
    };
    this.toggle = this.toggle.bind(this);

  }

  toggle() {
    this.setState({
      visible: !this.state.visible
    });
    const { snapshot } = this.props;
    let snapRoute = window.location.pathname + "/snapshots/" + snapshot["snapshot_id"];
    fetch(snapRoute)
      .then(res => res.json()).then(data => {
        data["attributes"].forEach(attribute => {
          if (attribute === "pose") {
            fetch(snapRoute + "/pose").then(res => res.json()).then(data => {
              let pose = JSON.parse(data["pose"][0]);
              let translation = pose["translation"];
              let rotation = pose["rotation"];
              this.setState({
                visible: this.state.visible,
                feelings: this.state.feelings,
                pose: {
                  "translation": "x=" + translation["x"] + ", y=" + translation["y"] + ", z=" + translation["z"],
                  "rotation": "x=" + rotation["x"] + ", y=" + rotation["y"] + ", z=" + rotation["z"] + ", w=" + rotation["w"]
                }
              });
            });
          }
          if (attribute === "feelings") {
            fetch(snapRoute + "/feelings").then(res => res.json()).then(data => {
              let getNum = num => Math.round(1000 * num);
              let feelings = JSON.parse(data["feelings"][0]);
              this.setState({
                visible: this.state.visible,
                pose: this.state.pose,
                feelings: {
                  labels: ['Hunger', 'Thirst', 'Exhaustion',
                           'Happiness'],
                  datasets: [
                    {
                      backgroundColor: 'rgba(0,0,255,1)',
                      borderColor: 'rgba(0,0,0,1)',
                      borderWidth: 1,
                      data: [ getNum(feelings["hunger"]), getNum(feelings["thirst"]),
                              getNum(feelings["exhaustion"]), getNum(feelings["happiness"])]
                    }
                  ]
                }
              });
            });
          }
        });
    });
  }

  render() {
    const { snapshot, ind } = this.props;
    let snapRoute = window.location.pathname + "/snapshots/" + snapshot["snapshot_id"];
    return (
      <Col className="col-lg mb-4 text-center" key={ind}>
       <Card>
        <CardBody>
          <CardTitle>
            {"Snapshot " + (ind + 1)}
          </CardTitle>
          <CardText>
            {snapshot["datetime"]}
          </CardText>
          <Button onClick={this.toggle}>more</Button>
            <Collapse open={this.state.visible}>
              <div className="p-3 mt-3 border rounded">
                <Tabs defaultActiveKey="color" transition={false} id="noanim-tab-example">
                  <Tab eventKey="color" title="Color">
                    <Card small className="stats-small--1">
                      <CardImg variant="middle" src={snapRoute + "/color_image/data"} style={{ maxWidth: "400px", maxHeight: "400px", alignSelf: 'center'}}>
                      </CardImg>
                    </Card>
                  </Tab>
                  <Tab eventKey="depth" title="Depth">
                    <Card small className="stats-small--1">
                      <CardImg variant="middle" src={snapRoute + "/depth_image/data"} style={{ maxWidth: "400px", maxHeight: "400px", alignSelf: 'center'}}>
                      </CardImg>
                    </Card>
                  </Tab>
                  <Tab eventKey="feelings" title="Feelings">
                    <Card small className="stats-small--1">
                      <Bar
                        data={this.state.feelings}
                        options={{ legend:{ display:false } }}
                      />
                    </Card>
                  </Tab>
                  <Tab eventKey="pose" title="Pose">
                    <Col className="col-lg mb-4 text-center" key={ind}>
                    <Card small className="stats-small--1 text-center">
                      <CardBody>
                        <CardTitle>
                          Translation
                        </CardTitle>
                        <CardText>
                          {this.state.pose["translation"]}
                        </CardText>
                      </CardBody>
                    </Card>
                    </Col>
                    <Col className="col-lg mb-4 text-center" key={ind}>
                    <Card small className="stats-small--1 text-center">
                      <CardBody>
                        <CardTitle>
                          Rotation
                        </CardTitle>
                        <CardText>
                          {this.state.pose["rotation"]}
                        </CardText>
                      </CardBody>
                    </Card>
                    </Col>
                  </Tab>
                </Tabs>
              </div>
            </Collapse>
        </CardBody>
      </Card>
      </Col>
    );
  }
}
