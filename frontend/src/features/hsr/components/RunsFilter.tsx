
import ReactDOM from 'react-dom';
import React, {useState} from 'react';
import { Button } from '../../../shared/ui/Button';
import Toggle from '../../../shared/ui/Toggle';

const RunsFilter = ({isOpen, onClose: onClose, children}: 
  {isOpen: boolean; onClose: () => void; children: React.ReactNode}) => {
  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <dialog
      id="filterDialog"
      open
      aria-modal="true"
      aria-labelledby="dialog-title"
      className="modal-dialog"
    >
      <h2 id="dialog-title" style={{display: 'flex', flexDirection: 'column'}}>Filter Dialog</h2>

      <Button onClick={onClose} variant="outline" style={{
        display: 'flex', 
        flexDirection: 'column', 
        justifyContent: 'flex-end'}}>Close</Button>

      <Toggle onChange={() => {
        console.log('Toggle onChange');
      } } value={false} name="Exclude chars" ></Toggle>
        
      
      <div className="modal-content">
        {children}
      </div>
    </dialog>,
    document.getElementById('modal-root') as HTMLElement
  );
} 

export default RunsFilter;