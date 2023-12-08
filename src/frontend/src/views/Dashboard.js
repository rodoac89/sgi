/*!

=========================================================
* Black Dashboard PRO React - v1.2.2
=========================================================

* Product Page: https://www.creative-tim.com/product/black-dashboard-pro-react
* Copyright 2023 Creative Tim (https://www.creative-tim.com)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React, { useState, useEffect } from "react";
// nodejs library that concatenates classes
import classNames from "classnames";
// react plugin used to create charts
import { Line, Bar } from "react-chartjs-2";
// react plugin for creating vector maps
import { VectorMap } from "react-jvectormap";

// reactstrap components
import {
  Button,
  ButtonGroup,
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  CardTitle,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  UncontrolledDropdown,
  Label,
  FormGroup,
  Input,
  Progress,
  Table,
  Row,
  Col,
  UncontrolledTooltip,
} from "reactstrap";

// core components
import {
  chartExample1,
  chartExample2,
  chartExample3,
  chartExample4,
} from "variables/charts.js";

var mapData = {
  AU: 760,
  BR: 550,
  CA: 120,
  DE: 1300,
  FR: 540,
  GB: 690,
  GE: 200,
  IN: 200,
  RO: 600,
  RU: 300,
  US: 2920,
};

const Dashboard = () => {
  let [chartData, setChartData] = useState({
    labels: ['1','2','3','4','5','6','7'] ,
    datasets: [
      {
        label: "Data",
        fill: true,
        borderColor: "#1f8ef1",
        borderWidth: 2,
        borderDash: [],
        borderDashOffset: 0.0,
        pointBackgroundColor: "#1f8ef1",
        pointBorderColor: "rgba(255,255,255,0)",
        pointHoverBackgroundColor: "#1f8ef1",
        pointBorderWidth: 20,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 15,
        pointRadius: 4,
        data: [0,0,0,0,0,0],
      },
    ]
  });
  const [bigChartData, setbigChartData] = React.useState("data1");
  const setBgChartData = (name) => {
    setbigChartData(name);
  };

  useEffect(() => {
    var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");

var raw = JSON.stringify({
  "ranges": [
    [
      1701529774623,
      1701572399999
    ],
    [
      1701572400000,
      1701658799999
    ],
    [
      1701658800000,
      1701745199999
    ],
    [
      1701745200000,
      1701831599999
    ],
    [
      1701831600000,
      1701917999999
    ],
    [
      1701918000000,
      1702004399999
    ],
    [
      1702004400000,
      1702048174623
    ]
  ],
  "room": "1"
});

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

///calculo de los ultimos 7 dias
const dias = ['DO', 'LU', 'MA', 'MI', 'JU', 'VI', 'SA'];

function getLast7Days() {
  const today = new Date();
  const daysArray = [];

  const day = today.getDay();

  for (let i = day; daysArray.length < 7; i = i === 0 ? 6 : (i - 1)) {
      const dayDate = dias[i];
      daysArray.push(dayDate);
  }

  return daysArray.reverse();
}

    fetch('http://127.0.0.1:8000/api/activity/session/chart', requestOptions)
    .then(
      async response => {
        console.log('recibo datos');
        var datos = await response.text();
        console.log("datos", JSON.parse(datos));

        setChartData({
            labels: getLast7Days(),
            datasets: [
              {
                label: "Data",
                fill: true,
                borderColor: "#1f8ef1",
                borderWidth: 2,
                borderDash: [],
                borderDashOffset: 0.0,
                pointBackgroundColor: "#1f8ef1",
                pointBorderColor: "rgba(255,255,255,0)",
                pointHoverBackgroundColor: "#1f8ef1",
                pointBorderWidth: 20,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 15,
                pointRadius: 4,
                data: JSON.parse(datos),
              },
            ]
          });
      }
    )
  }, [])
  return (
    <>
      <div className="content">
        <Row>
        <Col lg="4">
            <Card className="card-chart">
              <CardHeader>
                <h5 className="card-category">Últimos 7 días</h5>
                <CardTitle tag="h3">
                  <i className="tim-icons icon-bulb-63 text-primary" /> CO2 vs tiempo 
                </CardTitle>
              </CardHeader>
              <CardBody>
                <div className="chart-area">
                  <Line
                    data={chartData}
                    options={chartExample2.options}
                  />
                </div>
              </CardBody>
            </Card>
          </Col>
          <Col lg="4">
            <Card className="card-chart">
              <CardHeader>
                <h5 className="card-category">Daily Sales</h5>
                <CardTitle tag="h3">
                  <i className="tim-icons icon-delivery-fast text-info" />{" "}
                  3,500€
                </CardTitle>
              </CardHeader>
              <CardBody>
                <div className="chart-area">
                  <Bar
                    data={chartExample3.data}
                    options={chartExample3.options}
                  />
                </div>
              </CardBody>
            </Card>
          </Col>
          <Col lg="4">
            <Card className="card-chart">
              <CardHeader>
                <h5 className="card-category">Tickets abiertos</h5>
                <CardTitle tag="h3">
                  <i className="tim-icons icon-send text-success" /> 
                </CardTitle>
              </CardHeader>
              <CardBody>
                <div className="chart-area">
                  <Line
                    data={chartExample4.data}
                    options={chartExample4.options}
                  />
                </div>
              </CardBody>
            </Card>
          </Col>
          <Col lg="3" md="6">
            <Card className="card-stats">
              <CardBody>
                <Row>
                  <Col xs="5">
                    <div className="info-icon text-center icon-warning">
                      <i className="tim-icons icon-chat-33" />
                    </div>
                  </Col>
                  <Col xs="7">
                    <div className="numbers">
                      <p className="card-category">Number</p>
                      <CardTitle tag="h3">150GB</CardTitle>
                    </div>
                  </Col>
                </Row>
              </CardBody>
              <CardFooter>
                <hr />
                <div className="stats">
                  <i className="tim-icons icon-refresh-01" /> Update Now
                </div>
              </CardFooter>
            </Card>
          </Col>
          <Col lg="3" md="6">
            <Card className="card-stats">
              <CardBody>
                <Row>
                  <Col xs="5">
                    <div className="info-icon text-center icon-primary">
                      <i className="tim-icons icon-shape-star" />
                    </div>
                  </Col>
                  <Col xs="7">
                    <div className="numbers">
                      <p className="card-category">Followers</p>
                      <CardTitle tag="h3">+45k</CardTitle>
                    </div>
                  </Col>
                </Row>
              </CardBody>
              <CardFooter>
                <hr />
                <div className="stats">
                  <i className="tim-icons icon-sound-wave" /> Last Research
                </div>
              </CardFooter>
            </Card>
          </Col>
          <Col lg="3" md="6">
            <Card className="card-stats">
              <CardBody>
                <Row>
                  <Col xs="5">
                    <div className="info-icon text-center icon-success">
                      <i className="tim-icons icon-single-02" />
                    </div>
                  </Col>
                  <Col xs="7">
                    <div className="numbers">
                      <p className="card-category">Users</p>
                      <CardTitle tag="h3">150,000</CardTitle>
                    </div>
                  </Col>
                </Row>
              </CardBody>
              <CardFooter>
                <hr />
                <div className="stats">
                  <i className="tim-icons icon-trophy" /> Customers feedback
                </div>
              </CardFooter>
            </Card>
          </Col>
          <Col lg="3" md="6">
            <Card className="card-stats">
              <CardBody>
                <Row>
                  <Col xs="5">
                    <div className="info-icon text-center icon-danger">
                      <i className="tim-icons icon-molecule-40" />
                    </div>
                  </Col>
                  <Col xs="7">
                    <div className="numbers">
                      <p className="card-category">Errors</p>
                      <CardTitle tag="h3">12</CardTitle>
                    </div>
                  </Col>
                </Row>
              </CardBody>
              <CardFooter>
                <hr />
                <div className="stats">
                  <i className="tim-icons icon-watch-time" /> In the last hours
                </div>
              </CardFooter>
            </Card>
          </Col>
          
        </Row>
        <Row>
          <Col lg="5">
            <Card className="card-tasks">
              <CardHeader>
                <h6 className="title d-inline">Tasks(5)</h6>
                <p className="card-category d-inline">today</p>
                <UncontrolledDropdown>
                  <DropdownToggle
                    caret
                    className="btn-icon"
                    color="link"
                    data-toggle="dropdown"
                    type="button"
                  >
                    <i className="tim-icons icon-settings-gear-63" />
                  </DropdownToggle>
                  <DropdownMenu right>
                    <DropdownItem
                      href="#pablo"
                      onClick={(e) => e.preventDefault()}
                    >
                      Action
                    </DropdownItem>
                    <DropdownItem
                      href="#pablo"
                      onClick={(e) => e.preventDefault()}
                    >
                      Another action
                    </DropdownItem>
                    <DropdownItem
                      href="#pablo"
                      onClick={(e) => e.preventDefault()}
                    >
                      Something else
                    </DropdownItem>
                  </DropdownMenu>
                </UncontrolledDropdown>
              </CardHeader>
              <CardBody>
                <div className="table-full-width table-responsive">
                  <Table>
                    <tbody>
                      <tr>
                        <td>
                          <FormGroup check>
                            <Label check>
                              <Input defaultValue="" type="checkbox" />
                              <span className="form-check-sign">
                                <span className="check" />
                              </span>
                            </Label>
                          </FormGroup>
                        </td>
                        <td>
                          <p className="title">Update the Documentation</p>
                          <p className="text-muted">
                            Dwuamish Head, Seattle, WA 8:47 AM
                          </p>
                        </td>
                        <td className="td-actions text-right">
                          <Button
                            color="link"
                            id="tooltip786630859"
                            title=""
                            type="button"
                          >
                            <i className="tim-icons icon-pencil" />
                          </Button>
                          <UncontrolledTooltip
                            delay={0}
                            target="tooltip786630859"
                          >
                            Edit Task
                          </UncontrolledTooltip>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <FormGroup check>
                            <Label check>
                              <Input
                                defaultChecked
                                defaultValue=""
                                type="checkbox"
                              />
                              <span className="form-check-sign">
                                <span className="check" />
                              </span>
                            </Label>
                          </FormGroup>
                        </td>
                        <td>
                          <p className="title">GDPR Compliance</p>
                          <p className="text-muted">
                            The GDPR is a regulation that requires businesses to
                            protect the personal data and privacy of Europe
                            citizens for transactions that occur within EU
                            member states.
                          </p>
                        </td>
                        <td className="td-actions text-right">
                          <Button
                            color="link"
                            id="tooltip155151810"
                            title=""
                            type="button"
                          >
                            <i className="tim-icons icon-pencil" />
                          </Button>
                          <UncontrolledTooltip
                            delay={0}
                            target="tooltip155151810"
                          >
                            Edit Task
                          </UncontrolledTooltip>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <FormGroup check>
                            <Label check>
                              <Input defaultValue="" type="checkbox" />
                              <span className="form-check-sign">
                                <span className="check" />
                              </span>
                            </Label>
                          </FormGroup>
                        </td>
                        <td>
                          <p className="title">Solve the issues</p>
                          <p className="text-muted">
                            Fifty percent of all respondents said they would be
                            more likely to shop at a company
                          </p>
                        </td>
                        <td className="td-actions text-right">
                          <Button
                            color="link"
                            id="tooltip199559448"
                            title=""
                            type="button"
                          >
                            <i className="tim-icons icon-pencil" />
                          </Button>
                          <UncontrolledTooltip
                            delay={0}
                            target="tooltip199559448"
                          >
                            Edit Task
                          </UncontrolledTooltip>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <FormGroup check>
                            <Label check>
                              <Input defaultValue="" type="checkbox" />
                              <span className="form-check-sign">
                                <span className="check" />
                              </span>
                            </Label>
                          </FormGroup>
                        </td>
                        <td>
                          <p className="title">Release v2.0.0</p>
                          <p className="text-muted">
                            Ra Ave SW, Seattle, WA 98116, SUA 11:19 AM
                          </p>
                        </td>
                        <td className="td-actions text-right">
                          <Button
                            color="link"
                            id="tooltip989676508"
                            title=""
                            type="button"
                          >
                            <i className="tim-icons icon-pencil" />
                          </Button>
                          <UncontrolledTooltip
                            delay={0}
                            target="tooltip989676508"
                          >
                            Edit Task
                          </UncontrolledTooltip>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <FormGroup check>
                            <Label check>
                              <Input defaultValue="" type="checkbox" />
                              <span className="form-check-sign">
                                <span className="check" />
                              </span>
                            </Label>
                          </FormGroup>
                        </td>
                        <td>
                          <p className="title">Export the processed files</p>
                          <p className="text-muted">
                            The report also shows that consumers will not easily
                            forgive a company once a breach exposing their
                            personal data occurs.
                          </p>
                        </td>
                        <td className="td-actions text-right">
                          <Button
                            color="link"
                            id="tooltip557118868"
                            title=""
                            type="button"
                          >
                            <i className="tim-icons icon-pencil" />
                          </Button>
                          <UncontrolledTooltip
                            delay={0}
                            target="tooltip557118868"
                          >
                            Edit Task
                          </UncontrolledTooltip>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <FormGroup check>
                            <Label check>
                              <Input defaultValue="" type="checkbox" />
                              <span className="form-check-sign">
                                <span className="check" />
                              </span>
                            </Label>
                          </FormGroup>
                        </td>
                        <td>
                          <p className="title">Arival at export process</p>
                          <p className="text-muted">
                            Capitol Hill, Seattle, WA 12:34 AM
                          </p>
                        </td>
                        <td className="td-actions text-right">
                          <Button
                            color="link"
                            id="tooltip143185858"
                            title=""
                            type="button"
                          >
                            <i className="tim-icons icon-pencil" />
                          </Button>
                          <UncontrolledTooltip
                            delay={0}
                            target="tooltip143185858"
                          >
                            Edit Task
                          </UncontrolledTooltip>
                        </td>
                      </tr>
                    </tbody>
                  </Table>
                </div>
              </CardBody>
            </Card>
          </Col>
          <Col lg="7">
            <Card>
              <CardHeader>
                <div className="tools float-right">
                  <UncontrolledDropdown>
                    <DropdownToggle
                      caret
                      className="btn-icon"
                      color="link"
                      data-toggle="dropdown"
                      type="button"
                    >
                      <i className="tim-icons icon-settings-gear-63" />
                    </DropdownToggle>
                    <DropdownMenu right>
                      <DropdownItem
                        href="#pablo"
                        onClick={(e) => e.preventDefault()}
                      >
                        Action
                      </DropdownItem>
                      <DropdownItem
                        href="#pablo"
                        onClick={(e) => e.preventDefault()}
                      >
                        Another action
                      </DropdownItem>
                      <DropdownItem
                        href="#pablo"
                        onClick={(e) => e.preventDefault()}
                      >
                        Something else
                      </DropdownItem>
                      <DropdownItem
                        className="text-danger"
                        href="#pablo"
                        onClick={(e) => e.preventDefault()}
                      >
                        Remove Data
                      </DropdownItem>
                    </DropdownMenu>
                  </UncontrolledDropdown>
                </div>
                <CardTitle tag="h5">Management Table</CardTitle>
              </CardHeader>
              <CardBody>
                <Table responsive>
                  <thead className="text-primary">
                    <tr>
                      <th className="text-center">#</th>
                      <th>Name</th>
                      <th>Job Position</th>
                      <th>Milestone</th>
                      <th className="text-right">Salary</th>
                      <th className="text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td className="text-center">
                        <div className="photo">
                          <img
                            alt="..."
                            src={require("assets/img/tania.jpg")}
                          />
                        </div>
                      </td>
                      <td>Tania Mike</td>
                      <td>Develop</td>
                      <td className="text-center">
                        <div className="progress-container progress-sm">
                          <Progress multi>
                            <span className="progress-value">25%</span>
                            <Progress bar max="100" value="25" />
                          </Progress>
                        </div>
                      </td>
                      <td className="text-right">€ 99,225</td>
                      <td className="text-right">
                        <Button
                          className="btn-link btn-icon btn-neutral"
                          color="success"
                          id="tooltip618296632"
                          size="sm"
                          title="Refresh"
                          type="button"
                        >
                          <i className="tim-icons icon-refresh-01" />
                        </Button>
                        <UncontrolledTooltip
                          delay={0}
                          target="tooltip618296632"
                        >
                          Tooltip on top
                        </UncontrolledTooltip>
                        <Button
                          className="btn-link btn-icon btn-neutral"
                          color="danger"
                          id="tooltip707467505"
                          size="sm"
                          title="Delete"
                          type="button"
                        >
                          <i className="tim-icons icon-simple-remove" />
                        </Button>
                        <UncontrolledTooltip
                          delay={0}
                          target="tooltip707467505"
                        >
                          Tooltip on top
                        </UncontrolledTooltip>
                      </td>
                    </tr>
                    <tr>
                      <td className="text-center">
                        <div className="photo">
                          <img alt="..." src={require("assets/img/robi.jpg")} />
                        </div>
                      </td>
                      <td>John Doe</td>
                      <td>CEO</td>
                      <td className="text-center">
                        <div className="progress-container progress-sm">
                          <Progress multi>
                            <span className="progress-value">77%</span>
                            <Progress bar max="100" value="77" />
                          </Progress>
                        </div>
                      </td>
                      <td className="text-right">€ 89,241</td>
                      <td className="text-right">
                        <Button
                          className="btn-link btn-icon btn-neutral"
                          color="success"
                          id="tooltip216846074"
                          size="sm"
                          title="Refresh"
                          type="button"
                        >
                          <i className="tim-icons icon-refresh-01" />
                        </Button>
                        <UncontrolledTooltip
                          delay={0}
                          target="tooltip216846074"
                        >
                          Tooltip on top
                        </UncontrolledTooltip>
                        <Button
                          className="btn-link btn-icon btn-neutral"
                          color="danger"
                          id="tooltip391990405"
                          size="sm"
                          title="Delete"
                          type="button"
                        >
                          <i className="tim-icons icon-simple-remove" />
                        </Button>
                        <UncontrolledTooltip
                          delay={0}
                          target="tooltip391990405"
                        >
                          Tooltip on top
                        </UncontrolledTooltip>
                      </td>
                    </tr>
                    <tr>
                      <td className="text-center">
                        <div className="photo">
                          <img alt="..." src={require("assets/img/lora.jpg")} />
                        </div>
                      </td>
                      <td>Alexa Mike</td>
                      <td>Design</td>
                      <td className="text-center">
                        <div className="progress-container progress-sm">
                          <Progress multi>
                            <span className="progress-value">41%</span>
                            <Progress bar max="100" value="41" />
                          </Progress>
                        </div>
                      </td>
                      <td className="text-right">€ 92,144</td>
                      <td className="text-right">
                        <Button
                          className="btn-link btn-icon btn-neutral"
                          color="success"
                          id="tooltip191500186"
                          size="sm"
                          title="Refresh"
                          type="button"
                        >
                          <i className="tim-icons icon-refresh-01" />
                        </Button>
                        <UncontrolledTooltip
                          delay={0}
                          target="tooltip191500186"
                        >
                          Tooltip on top
                        </UncontrolledTooltip>
                        <Button
                          className="btn-link btn-icon btn-neutral"
                          color="danger"
                          id="tooltip320351170"
                          size="sm"
                          title="Delete"
                          type="button"
                        >
                          <i className="tim-icons icon-simple-remove" />
                        </Button>
                        <UncontrolledTooltip
                          delay={0}
                          target="tooltip320351170"
                        >
                          Tooltip on top
                        </UncontrolledTooltip>
                      </td>
                    </tr>
                    <tr>
                      <td className="text-center">
                        <div className="photo">
                          <img alt="..." src={require("assets/img/jana.jpg")} />
                        </div>
                      </td>
                      <td>Jana Monday</td>
                      <td>Marketing</td>
                      <td className="text-center">
                        <div className="progress-container progress-sm">
                          <Progress multi>
                            <span className="progress-value">50%</span>
                            <Progress bar max="100" value="50" />
                          </Progress>
                        </div>
                      </td>
                      <td className="text-right">€ 49,990</td>
                      <td className="text-right">
                        <Button
                          className="btn-link btn-icon"
                          color="success"
                          id="tooltip345411997"
                          size="sm"
                          title="Refresh"
                          type="button"
                        >
                          <i className="tim-icons icon-refresh-01" />
                        </Button>
                        <UncontrolledTooltip
                          delay={0}
                          target="tooltip345411997"
                        >
                          Tooltip on top
                        </UncontrolledTooltip>
                        <Button
                          className="btn-link btn-icon"
                          color="danger"
                          id="tooltip601343171"
                          size="sm"
                          title="Delete"
                          type="button"
                        >
                          <i className="tim-icons icon-simple-remove" />
                        </Button>
                        <UncontrolledTooltip
                          delay={0}
                          target="tooltip601343171"
                        >
                          Tooltip on top
                        </UncontrolledTooltip>
                      </td>
                    </tr>
                    <tr>
                      <td className="text-center">
                        <div className="photo">
                          <img alt="..." src={require("assets/img/mike.jpg")} />
                        </div>
                      </td>
                      <td>Paul Dickens</td>
                      <td>Develop</td>
                      <td className="text-center">
                        <div className="progress-container progress-sm">
                          <Progress multi>
                            <span className="progress-value">100%</span>
                            <Progress bar max="100" value="100" />
                          </Progress>
                        </div>
                      </td>
                      <td className="text-right">€ 69,201</td>
                      <td className="text-right">
                        <Button
                          className="btn-link btn-icon"
                          color="success"
                          id="tooltip774891382"
                          size="sm"
                          title="Refresh"
                          type="button"
                        >
                          <i className="tim-icons icon-refresh-01" />
                        </Button>
                        <UncontrolledTooltip
                          delay={0}
                          target="tooltip774891382"
                        >
                          Tooltip on top
                        </UncontrolledTooltip>
                        <Button
                          className="btn-link btn-icon"
                          color="danger"
                          id="tooltip949929353"
                          size="sm"
                          title="Delete"
                          type="button"
                        >
                          <i className="tim-icons icon-simple-remove" />
                        </Button>
                        <UncontrolledTooltip
                          delay={0}
                          target="tooltip949929353"
                        >
                          Tooltip on top
                        </UncontrolledTooltip>
                      </td>
                    </tr>
                    <tr>
                      <td className="text-center">
                        <div className="photo">
                          <img
                            alt="..."
                            src={require("assets/img/emilyz.jpg")}
                          />
                        </div>
                      </td>
                      <td>Manuela Rico</td>
                      <td>Manager</td>
                      <td className="text-center">
                        <div className="progress-container progress-sm">
                          <Progress multi>
                            <span className="progress-value">15%</span>
                            <Progress bar max="100" value="15" />
                          </Progress>
                        </div>
                      </td>
                      <td className="text-right">€ 99,201</td>
                      <td className="text-right">
                        <Button
                          className="btn-link btn-icon"
                          color="success"
                          id="tooltip30547133"
                          size="sm"
                          title="Refresh"
                          type="button"
                        >
                          <i className="tim-icons icon-refresh-01" />
                        </Button>
                        <UncontrolledTooltip delay={0} target="tooltip30547133">
                          Tooltip on top
                        </UncontrolledTooltip>
                        <Button
                          className="btn-link btn-icon"
                          color="danger"
                          id="tooltip156899243"
                          size="sm"
                          title="Delete"
                          type="button"
                        >
                          <i className="tim-icons icon-simple-remove" />
                        </Button>
                        <UncontrolledTooltip
                          delay={0}
                          target="tooltip156899243"
                        >
                          Tooltip on top
                        </UncontrolledTooltip>
                      </td>
                    </tr>
                  </tbody>
                </Table>
              </CardBody>
            </Card>
          </Col>
          <Col lg="12">
            <Card>
              <CardHeader>
                <CardTitle tag="h4">Global Sales by Top Locations</CardTitle>
                <p className="card-category">All products that were shipped</p>
              </CardHeader>
              <CardBody>
                <Row>
                  <Col md="6">
                    <Table responsive>
                      <tbody>
                        <tr>
                          <td>
                            <div className="flag">
                              <img
                                alt="..."
                                src={require("assets/img/US.png")}
                              />
                            </div>
                          </td>
                          <td>USA</td>
                          <td className="text-right">2.920</td>
                          <td className="text-right">53.23%</td>
                        </tr>
                        <tr>
                          <td>
                            <div className="flag">
                              <img
                                alt="..."
                                src={require("assets/img/DE.png")}
                              />
                            </div>
                          </td>
                          <td>Germany</td>
                          <td className="text-right">1.300</td>
                          <td className="text-right">20.43%</td>
                        </tr>
                        <tr>
                          <td>
                            <div className="flag">
                              <img
                                alt="..."
                                src={require("assets/img/AU.png")}
                              />
                            </div>
                          </td>
                          <td>Australia</td>
                          <td className="text-right">760</td>
                          <td className="text-right">10.35%</td>
                        </tr>
                        <tr>
                          <td>
                            <div className="flag">
                              <img
                                alt="..."
                                src={require("assets/img/GB.png")}
                              />
                            </div>
                          </td>
                          <td>United Kingdom</td>
                          <td className="text-right">690</td>
                          <td className="text-right">7.87%</td>
                        </tr>
                        <tr>
                          <td>
                            <div className="flag">
                              <img
                                alt="..."
                                src={require("assets/img/RO.png")}
                              />
                            </div>
                          </td>
                          <td>Romania</td>
                          <td className="text-right">600</td>
                          <td className="text-right">5.94%</td>
                        </tr>
                        <tr>
                          <td>
                            <div className="flag">
                              <img
                                alt="..."
                                src={require("assets/img/BR.png")}
                              />
                            </div>
                          </td>
                          <td>Brasil</td>
                          <td className="text-right">550</td>
                          <td className="text-right">4.34%</td>
                        </tr>
                      </tbody>
                    </Table>
                  </Col>
                  <Col className="ml-auto mr-auto" md="6">
                    <VectorMap
                      map={"world_mill"}
                      backgroundColor="transparent"
                      zoomOnScroll={false}
                      containerStyle={{
                        width: "100%",
                        height: "300px",
                      }}
                      regionStyle={{
                        initial: {
                          fill: "#e4e4e4",
                          "fill-opacity": 0.9,
                          stroke: "none",
                          "stroke-width": 0,
                          "stroke-opacity": 0,
                        },
                      }}
                      series={{
                        regions: [
                          {
                            values: mapData,
                            scale: ["#AAAAAA", "#444444"],
                            normalizeFunction: "polynomial",
                          },
                        ],
                      }}
                    />
                  </Col>
                </Row>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    </>
  );
};

export default Dashboard;