import React from "react";
import {
  Badge,
  Collapse,
  DropdownItem,
  Col, Card, CardBody, CardImg, CardTitle, CardText, Button, Row
} from "shards-react";
import { Nav, NavItem, NavLink } from "shards-react";

export default class Snapshot extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      visible: false,
      feelings: undefined,
      pose: undefined,
      colorImage: undefined,
      depthImage: undefined
    };
    this.toggle = this.toggle.bind(this);

  }

  toggle() {
    console.log("toggle!!!!!");
    this.setState({
      visible: !this.state.visible
    });
    const { snapshot } = this.props;
    let snapRoute = window.location.pathname + "/snapshots/" + snapshot["snapshot_id"];
    fetch(snapRoute)
      .then(res => res.json()).then(data => {
        console.log(data);
        data["attributes"].forEach(attribute => {
          console.log("attribute=" + attribute);
          if (attribute === "pose") {
            console.log("got pose###");
            console.log(attribute);
          }
          if (attribute === "feelings") {

          }
          if (attribute === "depth_image") {

          }
        });



    });
  }

  render() {
    const { snapshot, ind } = this.props;
    let snapRoute = window.location.pathname + "/snapshots/" + snapshot["snapshot_id"];
    return (
      <Row key={ind}>
            <Col className="col-lg mb-4 text-center">
             <Card small className="stats-small--1">
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
                      <Row>
                        <Col className="col-lg mb-4" md="6" sm="6">
                          <Card small className="stats-small--1">
                            <CardImg variant="middle" src={snapRoute + "/color_image/data"} style={{ maxWidth: "400px", maxHeight: "400px", alignSelf: 'center'}}>
                            </CardImg>
                          </Card>
                        </Col>
                        <Col className="col-lg mb-4" md="6" sm="6">
                          <Card small className="stats-small--1">
                            <CardImg variant="middle" src={snapRoute + "/depth_image/data"} style={{ maxWidth: "400px", maxHeight: "400px", alignSelf: 'center'}}>
                            </CardImg>
                          </Card>
                        </Col>
                      </Row>
                    </div>
                  </Collapse>
              </CardBody>
            </Card>
            </Col>
          </Row>
    );
  }
}
