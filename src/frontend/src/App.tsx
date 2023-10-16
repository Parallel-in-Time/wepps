import '../node_modules/uikit/dist/css/uikit.css';
import '../node_modules/uikit/dist/js/uikit.min';
import '../node_modules/uikit/dist/js/uikit-icons.min.js';

import axios from 'axios';

import Stages from './stages/Stages';
import {
  DocumentationButton,
  DocumentationModal,
  HomeButton,
} from './StaticElements.js';
import { useEffect, useState } from 'react';

function Title() {
  return (
    <div className='uk-width-1-1'>
      <h1 className='uk-heading uk-heading-line uk-text-center'>
        <span> {document.title} </span>
      </h1>
    </div>
  );
}

function App() {
  const [visibleModal, setVisibleModal] = useState(false);
  const [documentation, setDocumentation] = useState('');

  // Get the documentation text once
  useEffect(() => {
    axios.get(`${window.location.pathname}/documentation`).then((response) => {
      setDocumentation(response.data.text);
    });
  }, []);

  const modal = visibleModal ? (
    <DocumentationModal
      text={documentation}
      toggleVisibility={setVisibleModal}
    />
  ) : (
    <></>
  );

  function toggleVisibility() {
    setVisibleModal((m) => !m);
  }

  return (
    <>
      <HomeButton />
      <DocumentationButton toggleVisibility={toggleVisibility} />
      {modal}
      <div className='uk-height-1-1 uk-padding uk-background-muted'>
        <div className='uk-container uk-container-expand'>
          <Title />

          <Stages />
        </div>
      </div>
    </>
  );
}

export default App;
