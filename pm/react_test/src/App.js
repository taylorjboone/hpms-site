// Render Prop
import React from 'react';
import { useState } from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import Button from '@mui/material/Button';
import axios from 'axios';

const labelMap = {id:'id', route_id: 'Route ID', bmp: 'BMP', emp: 'EMP', org_num: 'Org #', project_name: 'Project Name', activity_code: 'Activity Code', activity_description: 'Activity Description', route_name: 'Route Name', accomplishments: 'Accomplishments', units: 'Units', crew_members: 'Crew Members', travel_hours: 'Travel Hours', onsite_hours: 'On-Site', task_date: 'Task Date', notes: 'Notes' }
const activityCodes = {
132: {"Activity Description": "Materials Investiagtion and Test Borings", "Unit of Measure": "Employee Hours (EH)"}, 
201: {"Activity Description": "Patching of Bituminous Pavements","Unit of Measure": "Tons (TN)"},
202: {"Activity Description": "Repair of Base Failure", "Unit of Measure": "Tons (TN)"},
203: {"Activity Description": "Skip Patching", "Unit of Measure": "Tons (TN)"},
204: {"Activity Description": "Sealing and Surface Treatment", "Unit of Measure": "Tons (TN)"},
205: {"Activity Description": "Tack Coat", "Unit of Measure": "Gallons (GA)"},
206: {"Activity Description": "Purchase Order Contract Paving", "Unit of Measure": "Dollars (DL)"},
207: {"Activity Description": "Hand or Machine Patching  & Sealing with Asphalt & Aggregate", "Unit of Measure": "Tons (TN)"},
208: {"Activity Description": "Joint and Crack Sealing in Flexible Pavements", "Unit of Measure": "Feet (FT)"},
209: {"Activity Description": "Temporary Patch \u2014 PREMIX", "Unit of Measure": "Tons (TN)"},
210: {"Activity Description": "Paving", "Unit of Measure": "Tons (TN)"},
241: {"Activity Description": "Patching PCC Pavements", "Unit of Measure": "Square Feet (SF)"},
244: {"Activity Description": "Joint and Crack Sealing in PCC Pavements", "Unit of Measure": "Feet (FI)"},
245: {"Activity Description": "Surface Repair of PCC Pavements", "Unit of Measure": "Square Feet (SF)"},
246: {"Activity Description": "Patching PCC Pavements with Premix", "Unit of Measure": "Tons (TN)"},
260: {"Activity Description": "Stabilization - Shoulders", "Unit of Measure": "Tons (TN)"},
261: {"Activity Description": "Stabilization - Roadway", "Unit of Measure": "Tons (TN)"},
262: {"Activity Description": "Ditching & Blading \u2014 Unpaved Roadway", "Unit of Measure": "Miles (MI)"},
263: {"Activity Description": "Blading \u2014 Unpaved Roadway", "Unit of Measure": "Miles (MI)"},
280: {"Activity Description": "Install Temporary Pipe Culverts", "Unit of Measure": "Feet (FT)"},
281: {"Activity Description": "Minor Drainage Structures", "Unit of Measure": "Employee Hours (EH)"},
282: {"Activity Description": "Install Pipe Culverts", "Unit of Measure": "Feet (FT)"},
283: {"Activity Description": "Subsurface Drains", "Unit of Measure": "Feet (FT)"},
284: {"Activity Description": "Dumped Rock Ditches", "Unit of Measure": "Tons (TN)"},
285: {"Activity Description": "Riprapping of Embankments", "Unit of Measure": "Tons (TN)"},
286: {"Activity Description": "Installation and Maintenance of Non-Bridge Structures", "Unit of Measure": "Employee Hours (EH)"},
287: {"Activity Description": "Removing Ditchline Obstacles", "Unit of Measure": "Feet (FT)"},
288: {"Activity Description": "Pulling Shoulders or Ditches Paved Roadway", "Unit of Measure": "Shoulder Miles (SM)"},
289: {"Activity Description": "Dressing Shoulders Under Guardrail", "Unit of Measure": "Feet (FT)"},
290: {"Activity Description": "lnstall Large Pipe Culverts", "Unit of Measure": "Feet (FT)"},
301: {"Activity Description": "Guardrail Maintenance", "Unit of Measure": "Feet (FT)"},
302: {"Activity Description": "Repair/Replace Rights-of-Way Fence", "Unit of Measure": "Feet (FT)"},
303: {"Activity Description": "Mowing -  Non-Expressway", "Unit of Measure": "Shoulder Miles (SM)"},
304: {"Activity Description": "Brush Control - Hand", "Unit of Measure": "Employee Hours (EH)"},
305: {"Activity Description": "Brush Control \u2014 Machine", "Unit of Measure": "Shoulder Miles (SM)"},
306: {"Activity Description": "Wildflowers", "Unit of Measure": "Acre (AC)"},
307: {"Activity Description": "Herbicide Spraying", "Unit of Measure": "Acre (AC)"},
308: {"Activity Description": "Litter Pickup and Disposal", "Unit of Measure": "Bags (BG)"},
309: {"Activity Description": "Rest Area Maintenance", "Unit of Measure": "Employee Hours (EH)"},
310: {"Activity Description": "Dead Animal \u2014 NOT Deer \u2014 Pickup/ Removal", "Unit of Measure": "Employee Hours (EH)"},
312: {"Activity Description": "Litter Disposal / Support (Non-DOH Forces)", "Unit of Measure": "Employee Hours (EH)"},
313: {"Activity Description": "Contract / Hired Maintenance", "Unit of Measure": "Dollars (DL)"},
314: {"Activity Description": "Supervision -  Work Release Program", "Unit of Measure": "Employee Hours (EH)"},
315: {"Activity Description": "Dead Deer \u2014 Pickup/Removal", "Unit of Measure": "Employee Hours (EH)"},
316: {"Activity Description": "Hand Mowing/ Trimming", "Unit of Measure": "Employee Hours (EH)"},
317: {"Activity Description": "Mowing - Expressway", "Unit of Measure": "Acre (AC)"},
318: {"Activity Description": "Canopy Clearing", "Unit of Measure": "Acre (AC)"},
319: {"Activity Description": "Hazard Tree Removal", "Unit of Measure": "Employee Hours (EH)"},
340: {"Activity Description": "Anti-Icing or Deicing with Brine", "Unit of Measure": "Gallons (GA)"},
341: {"Activity Description": "Mechanical Application of SRIC Materials", "Unit of Measure": "Tons (TN)"},
342: {"Activity Description": "Snow Plowing or Blowing", "Unit of Measure": "Employee Hours (EH)"},
343: {"Activity Description": "Snow Fence", "Unit of Measure": "Feet (FT)"},
344: {"Activity Description": "SRIC Post Storm Cleanup", "Unit of Measure": "Employee Hours (EH)"},
345: {"Activity Description": "SRIC Support Operations", "Unit of Measure": "Employee Hours (EH)"},
361: {"Activity Description": "Coding and Spotting", "Unit of Measure": "Miles (MI)"},
362: {"Activity Description": "ITS", "Unit of Measure": "Employee Hours (EH)"},
363: {"Activity Description": "Pavement Markings", "Unit of Measure": "Employee Hours (EH)"},
364: {"Activity Description": "Sign Installation / Maintenance", "Unit of Measure": "Employee Hours (EH)"},
365: {"Activity Description": "Traffic Signals", "Unit of Measure": "Employee Hours (EH)"},
366: {"Activity Description": "Impact Attenuators", "Unit of Measure": "Each (EA)"},
368: {"Activity Description": "Roadway Striping", "Unit of Measure": "Miles (MI)"},
369: {"Activity Description": "Highway Lights", "Unit of Measure": "Miles (MI)"},
370: {"Activity Description": "Install/Repair Overhead Sign Structures", "Unit of Measure": "Employee Hours (EH)"},
381: {"Activity Description": "Bridge Structure Replacement", "Unit of Measure": "Employee Hours (EH)"},
382: {"Activity Description": "Bridge Inspection & Analysis", "Unit of Measure": "Employee Hours (EH)"},
383: {"Activity Description": "Bridge Design", "Unit of Measure": "Employee Hours (EH)"},
384: {"Activity Description": "Cleaning and Painting", "Unit of Measure": "Employee Hours (EH)"},
385: {"Activity Description": "Repair and Realignment of Bearing Devices", "Unit of Measure": "Employee Hours (EH)"},
386: {"Activity Description": "Repair/ Replacement of Expansion Dam Seals", "Unit of Measure": "Employee Hours (EH)"},
387: {"Activity Description": "Sealing of Concrete Bridge Decks", "Unit of Measure": "Employee Hours (EH)"},
388: {"Activity Description": "Sealing of Bridge Concrete Substructure Units", "Unit of Measure": "Employee Hours (EH)"},
389: {"Activity Description": "Bridge Washing", "Unit of Measure": "Employee Hours (EH)"},
390: {"Activity Description": "Opening of Bridge Drainage Systems", "Unit of Measure": "Employee Hours (EH)"},
391: {"Activity Description": "Scour / Erosion & Riprapping at Bridges", "Unit of Measure": "Employee Hours (EH)"},
392: {"Activity Description": "Bridge Deck Repair", "Unit of Measure": "Employee Hours (EH)"},
393: {"Activity Description": "Bridge Deck Replacement", "Unit of Measure": "Employee Hours (EH)"},
394: {"Activity Description": "Bridge Superstructure Repair", "Unit of Measure": "Employee Hours (EH)"},
395: {"Activity Description": "Bridge Superstructure Replacement", "Unit of Measure": "Employee Hours (EH)"},
396: {"Activity Description": "Bridge Substructure Repair", "Unit of Measure": "Employee Hours (EH)"},
397: {"Activity Description": "Bridge Deck Overlays", "Unit of Measure": "Employee Hours (EH)"},
398: {"Activity Description": "Bridge Culvert Repair", "Unit of Measure": "Employee Hours (EH)"},
399: {"Activity Description": "Bridge Culvert Replacement", "Unit of Measure": "Employee Hours (EH)"},
401: {"Activity Description": "Asphalt Pavement Grinding", "Unit of Measure": "Square Yards (SY)"},
402: {"Activity Description": "Sweeping", "Unit of Measure": "Employee Hours (EH)"},
403: {"Activity Description": "Tunnel Maintenance", "Unit of Measure": "Employee Hours (EH)"},
404: {"Activity Description": "Emergency Services", "Unit of Measure": "Employee Hours (EH)"},
405: {"Activity Description": "Steel Piling Installation", "Unit of Measure": "Feet (FT)"},
406: {"Activity Description": "Unclassified Excavation", "Unit of Measure": "Tons (TN)"},
407: {"Activity Description": "Non-Annual Plan Employee Hours", "Unit of Measure": "Employee Hours (EH)"},
408: {"Activity Description": "Miscellaneous Maintenance", "Unit of Measure": "Employee Hours (EH)"},
409: {"Activity Description": "Placing PCC", "Unit of Measure": "Cubic Yards (CY)"},
410: {"Activity Description": "Erosion / Pollution Control", "Unit of Measure": "Employee Hours (EH)"},
411: {"Activity Description": "Hauling Materials -  Premix and Stone", "Unit of Measure": "Miles (MI)"},
412: {"Activity Description": "Embankment  Stabilization - DOH", "Unit of Measure": "Tons (TN)"},
413: {"Activity Description": "Embankment Stabilisation - Contract", "Unit of Measure": "Dollars (DL)"},
414: {"Activity Description": "Oil and Gas Road Policy Encroachment Permitting", "Unit of Measure": "Employee Hours (EH)"},
415: {"Activity Description": "Oil and Gas Road Policy Permit Inspections and Administration", "Unit of Measure": "Employee Hours (EH)"},
416: {"Activity Description": "Emergency / Cooperative Oil and Gas Road Repair", "Unit of Measure": "Employee Hours (EH)"},
417: {"Activity Description": "lnstall Gabion Baskets, Crib Walls and Concr\u00e8te Block Walls", "Unit of Measure": "Cubic Yards (CY)"},
420: {"Activity Description": "Natural Disaster Debris Removal", "Unit of Measure": "Cubic Yards (CY)"},
421: {"Activity Description": "Geostabilization Support", "Unit of Measure": "Employee Hours (EH)"},
501: {"Activity Description": "Equipment Down Time", "Unit of Measure": "Employee Hours (EH)"},
529: {"Activity Description": "Repair of Hired/ Rented Equipment", "Unit of Measure": "Employee Hours (EH)"},
535: {"Activity Description": "Mounting / Dismounting Attachments to Equipment for Temporary Use", "Unit of Measure": "Employee Hours (EH)"},
542: {"Activity Description": "Equipment Transporting -  All", "Unit of Measure": "Employee Hours (EH)"},
550: {"Activity Description": "Equipment Shop Overhead", "Unit of Measure": "Employee Hours (EH)"},
568: {"Activity Description": "Miscellaneous  Expenses Equipment Shop", "Unit of Measure": "Dollars (DL)"},
801: {"Activity Description": "Organization Overhead", "Unit of Measure": "Employee Hours (EH)"},
802: {"Activity Description": "Miscellaneous Inventory Exp - Maintenance", "Unit of Measure": "Dollars (DL)"},
803: {"Activity Description": "Leave Time", "Unit of Measure": "Employee Hours (EH)"},
807: {"Activity Description": "Grievance \u2014 Maintenance Work Force", "Unit of Measure": "Employee Hours (EH)"},
809: {"Activity Description": "Training", "Unit of Measure": "Employee Hours (EH)"},
811: {"Activity Description": "Unproductive Equipment", "Unit of Measure": "Dollars (DL)"},
812: {"Activity Description": "Rents and Miscellaneous Expenses", "Unit of Measure": "Dollars (DL)"},
813: {"Activity Description": "Flagging", "Unit of Measure": "Employee Hours (EH)"},
814: {"Activity Description": "Handling of Materials (Non-SRlC)", "Unit of Measure": "Employee Hours (EH)"},
815: {"Activity Description": "Cleaning of Equipment", "Unit of Measure": "Employee Hours (EH)"},
816: {"Activity Description": "Building and Grounds", "Unit of Measure": "Employee Hours (EH)"},
817: {"Activity Description": "SWAT/Citizen Requests", "Unit of Measure": "Employee Hours (EH)"}}

const Basic = () => {

  const [taskData, setTaskData] = useState(null)

function getData(data) {
  axios({
    method: "GET",
    url:"",
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
                } else if (k == 'activity_code') {
                    return <td><Field type="" name={k} style={{width:"7em", textAlign:"center"}}/></td>
                } else if (k !== 'id') {
                    return <td><Field type="" name={k} style={{width:"95%", textAlign:"center"}}/></td>
                } else if (k == 'task_date') {
                    return <td><Field type="date" name={k}/></td>
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