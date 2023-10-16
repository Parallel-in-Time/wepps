import Docs from './Docs';
import Plots from './Plots';
import Settings from './Settings';

import InfoBar from '../infobar/InfoBar';

import axios from 'axios';
import { useEffect, useState } from 'react';
import { ParameterValue } from './Interfaces';

interface Parameters {
  [stage: string]: {
    [id: string]: {
      id: string;
      name: string;
      value: string;
      isValid: boolean;
      stage: string;
    };
  };
}

function Stages() {
  // The received data which are only changed, whenever the compute request is sent
  const [docsData, setDocsData] = useState([]);
  const [settingsData, setSettingsData] = useState([]);
  const [plotsData, setPlotsData] = useState([]);

  // The parameter values which are sent back to the server
  const [parameters, setParameters] = useState<Parameters>({});

  // The invalid parameters that define the errors in the info bar
  const [invalidParameters, setInvalidParameters] = useState<string[]>([]);

  // Compute sends the data and sets the returned data into this stage
  function computeCallback() {
    // Pack up the paramters into a compact object that will be send
    const data: {
      [stage: string]: { [id: string]: string };
    } = {};
    Object.keys(parameters).forEach((stageKey) => {
      const stage = parameters[stageKey];
      data[stageKey] = {};
      Object.keys(stage).forEach((parameterKey) => {
        data[stageKey][parameterKey] = stage[parameterKey].value;
      });
    });

    // Add a computing spinner
    // @ts-expect-error
    let notification = null;
    if (Object.keys(data).length > 0) {
      // @ts-expect-error
      notification = UIkit.notification({
        message: '<div uk-spinner></div> &nbsp; Computing...',
        pos: 'top-center',
        timeout: 0,
      });
    }

    axios
      .post(`${window.location.pathname}/compute`, data)
      .then((response) => {
        // Remove the spinner if it exists
        // @ts-expect-error
        if (notification !== null) notification.close();

        // Set all stages with the data
        setDocsData(() => response.data.docs);
        setSettingsData(() => response.data.settings);
        setPlotsData(() => response.data.plots);
      })
      .catch((error) => {
        // Remove the spinner if it exists
        // @ts-expect-error
        if (notification !== null) notification.close();

        if (error.response.status === 400) {
          // @ts-expect-error
          UIkit.notification(error.response.data, 'danger');
        }
      });
  }

  // On startup, send one initial compute request
  useEffect(() => computeCallback(), []);

  // The update parameter callback function that is passed down to the input fields
  const updateParameter = (stage: string, parameter: ParameterValue) => {
    // Set the parameters
    setParameters((params: Parameters) => {
      const param = {
        id: parameter.id,
        name: parameter.name,
        value: parameter.value,
        isValid: parameter.isValid,
        stage: stage,
      };

      // Return the updated parameters
      return {
        ...params,
        [stage]: { ...params[stage], [parameter.id]: param },
      };
    });
  };

  useEffect(() => {
    Object.keys(parameters).forEach((stageKey) => {
      const stage = parameters[stageKey];
      Object.keys(stage).forEach((parameterKey) => {
        const parameter = stage[parameterKey];

        // Filter the correct stageTitle from the corresponding stage
        const stageTitle = settingsData.filter((e) => e['id'] === stageKey)[0][
          'title'
        ];

        const infoText = `${stageTitle}: ${parameter.name}`;
        // Whenever the parametrs change, look out for the invalid parameters
        // Check if its not included but invalid
        const exists = invalidParameters.indexOf(infoText);
        if (exists === -1 && !parameter.isValid) {
          // Then add it
          setInvalidParameters((p) => [...p, infoText]);
        } else if (
          invalidParameters.indexOf(infoText) !== -1 &&
          parameter.isValid
        ) {
          // Check if this parameters is already included but is actually valid
          // Then remove it
          setInvalidParameters((p) => p.filter((e) => e !== infoText));
        }
      });
    });
  }, [parameters]);

  return (
    <>
      <InfoBar
        invalidParameters={invalidParameters}
        parameters={parameters}
        computeCallback={computeCallback}
      />

      <div className='uk-width-1-1'>
        <div className='uk-child-width-1-3@m uk-grid-column-small' data-uk-grid>
          <div>
            <Docs docs={docsData} />
          </div>
          <div>
            <Settings
              settings={settingsData}
              updateParameter={updateParameter}
            />
          </div>
          <div>
            <Plots plots={plotsData} />
          </div>
        </div>
      </div>
    </>
  );
}
export default Stages;
