// Render Prop
import React from 'react';
import { useState } from 'react';
import { Formik, Form, Field, ErrorMessage, InputNumber } from 'formik';
import * as Yup from 'yup';
import Button from '@mui/material/Button';
import axios from 'axios';
import { activityCodes, labelMap, orgNums } from './consts';



const Basic = () => {

  const [taskData, setTaskData] = useState(null)

function getData(data) {
  axios({
    method: "GET",
    url:"/pm/work_plan/apply_edits",
  })
  .then((response) => {
    const res = response.data
    setTaskData(({
      id: res.id,
      route_id: res.route_id,
      bmp: res.bmp,
      emp: res.emp,
      org_num: res.org_num,
      project_name: res.project_name,
      activity_code: res.activity_code,
      activity_description: res.activity_description,
      route_name: res.route_name,
      accomplishments: res.accomplishments,
      units: res.units,
      crew_members: res.crew_members,
      travel_hours: res.travel_hours,
      onsite_hours: res.onsite_hours,
      task_date: res.task_date,
      notes: res.notes}))
  }).catch((error) => {
    if (error.response) {
      console.log(error.response)
      console.log(error.response.status)
      console.log(error.response.headers)
    }
  })
}
function postData(data) {
  alert(JSON.stringify(data))
  axios({
    method: 'post',
    url: '/pm/work_plan/apply_edits',
    data: data
  })
  .then(function (response) {
    console.log(response);
  }).catch(function (error) {
    console.log(error);
  })
}
  return <div style={{ width: "100%", overflow: 'auto'}}>
    <h1>Task Information</h1>
    <Formik
      initialValues={{
                      route_id: '',
                      bmp: '',
                      emp: '',
                      org_num: '',
                      project_name: '',
                      activity_code: '',
                      activity_description: '',
                      route_name: '',
                      accomplishments: '',
                      units: '',
                      crew_members: '',
                      travel_hours: '',
                      onsite_hours: '',
                      task_date: '',
                      notes: '' }}
  validationSchema={Yup.object({
    route_id: Yup.string()
      .min(13, 'Route ID must be 13 characters at minimum')
      .max(18, 'Route ID can only be 18 characters at maximum')
      .required('Required'),
    bmp: Yup.number()
      .required('Required'),
    emp: Yup.number()
      .required('Required'),
    org_num: Yup.string()
      .required('Required'),
    project_name: Yup.string()
      .required('Required'),
    activity_code: Yup.number()
      .required('Required'),
  })}
  onSubmit={(values, { setSubmitting }) => {
      alert("DSL:FJKSDL:FJ")
      setSubmitting(true);
      postData({adds:[values]})
      setSubmitting(false)
  }}
    >
      {({ isSubmitting, values, errors, touched }) => (
        <Form>
          <table>
            <thead>
              {Object.keys(values).map((k)=>{
              var v = labelMap[k];
              if (k == 'activity_code') {
                  return <th><label for={k} style={{width:'-webkit-fill-available'}}>{v}</label></th>
              } else if (k !== 'id') {
                  return <th><label for={k}>{v}</label></th>
              } else {
                return <></>
              }
              })}
            </thead>
            <tr>
              {Object.keys(values).map((k)=>{
                var v = values[k]
                if (k == 'route_id') {
                    return <td><Field type="" name={k} style={{width:"10.5em", textAlign:"center"}}/></td>
                } else if (['bmp','emp','org_num'].includes(k)) {
                    return <td><Field type="" name={k} style={{width:"3em", textAlign:"center"}}/></td>
                } else if (k == 'activity_code'||k=="crew_members") {
                    return <td><Field type="number" name={k} style={{width:"7em", textAlign:"center"}}/></td>
                } else if (k !== 'id') {
                    return <td><Field type="" name={k} style={{width:"95%", textAlign:"center"}}/></td>
                } else if (k == 'task_date') {
                    return <td><Field type="date" name={k}/></td>
                }
              })}
            </tr>


            <tr>
              {Object.keys(values).map((k)=>{
                if (errors[k] && touched[k]) {
                  return <ErrorMessage name={k} component="td"/>
                } else {
                  return <td><ErrorMessage name={k} component="td"  width='20px'/></td>
                }
              })}
            </tr>
          </table>
          
          <Button type='submit' variant='contained' disabled={isSubmitting} style={{'margin': '1% 0 0 95%'}} size='small'>
            Submit
          </Button>

        </Form>
      )}
    </Formik>
  </div>
};

export default Basic;