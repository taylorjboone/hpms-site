// Render Prop
import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import Button from '@mui/material/Button';

const labelMap = { route_id: 'Route ID', bmp: 'BMP', emp: 'EMP', org_num: 'Organization Number', project_name: 'Project Name', activity_code: 'Activity Code', activity_description: 'Activity Description', route_name: 'Route Name', accomplishments: 'Accomplishments', units: 'Units', crew_members: 'Crew Members', travel_hours: 'Travel Hours', onsite_hours: 'On-Site', task_date: 'Task Date', notes: 'Notes' }

const Basic = () => {
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
      setTimeout(() => {
          alert(JSON.stringify(values, null, 2));
          setSubmitting(false);
      }, 500);
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
                if (k == 'task_date') {
                  return <td><Field type="date" name={k}/></td>
                } else if (k !== 'id') {
                  return <td><Field type="" name={k} style={{width:"90%", textAlign:"center"}}/></td>
                } 
              })}
            </tr>
            <tr>
              {Object.keys(values).map((k)=>{
                if (errors[k] && touched[k]) {
                  return <ErrorMessage name={k} component="td"/>
                } else {
                  return <td><ErrorMessage name={k} component="td"  width='5px'/></td>
                }
              })}
            </tr>
          </table>
          
          <Button type='submit' variant='contained' disabled={isSubmitting}>
            Submit
          </Button>

        </Form>
      )}
    </Formik>
  </div>
};

export default Basic;