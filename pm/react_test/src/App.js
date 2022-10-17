// Render Prop
import React from 'react';
import { useState } from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import Button from '@mui/material/Button';
import axios from 'axios';

const labelMap = {id:'id', route_id: 'Route ID', bmp: 'BMP', emp: 'EMP', org_num: 'Org #', project_name: 'Project Name', activity_code: 'Activity Code', activity_description: 'Activity Description', route_name: 'Route Name', accomplishments: 'Accomplishments', units: 'Units', crew_members: 'Crew Members', travel_hours: 'Travel Hours', onsite_hours: 'On-Site', task_date: 'Task Date', notes: 'Notes' }




const Basic = () => {

  const [taskData, setTaskData] = useState(null)

function getData(data) {
  axios({
    method: "GET",
    url:"/pm/work_plan/api",
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
  axios({
    method: 'post',
    url: '/pm/work_plan/api',
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
      initialValues={{ id: '',
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
    activity_code: Yup.string()
      .required('Required'),
  })}
  onSubmit={(values, { setSubmitting }) => {
      setSubmitting(true);
      postData(values)
      setSubmitting(false)
      // setTimeout(() => {
      //     alert(JSON.stringify(values, null, 2));
      //     setSubmitting(false);
      // }, 500);
  }}
    >
      {({ isSubmitting, values, errors, touched }) => (
        <Form>
          <table>
            <thead>
              {Object.keys(values).map((k)=>{
              var v = labelMap[k];
              if (k !== 'id') {
                  return <th><label for={k}>{v}</label></th>
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
                } else if (k !== 'id') {
                    return <td><Field type="" name={k} style={{width:"85%", textAlign:"center"}}/></td>
                } else if (k == 'task_date') {
                  return <td><Field type="date" name={k}/></td>
                }
              })}
            </tr>
          </table>
          
          <Button type='submit' variant='contained' disabled={isSubmitting} style={{'margin': '0 0 0 95%'}}>
            Submit
          </Button>

        </Form>
      )}
    </Formik>
  </div>
};

export default Basic;