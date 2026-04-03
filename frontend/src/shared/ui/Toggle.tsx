import React, { useRef } from 'react'
import PropTypes from 'prop-types'
Toggle.propTypes = {
  onChange: PropTypes.func,
  value: PropTypes.string,
  name: PropTypes.string,
  checked: PropTypes.bool
}
export default function Toggle(props: { 
  onChange: () => void; 
  name: string | undefined; 
  value: boolean | undefined; 
  checked: any 
}) {
  const toggle = useRef<HTMLSpanElement>(null)
  const checkbox = useRef<HTMLInputElement>(null)
  function handleToggle() {
    if (props.onChange) props.onChange()
    if (toggle.current) {
      toggle.current.classList.toggle('toggled')
    }
    if (checkbox.current) {
      checkbox.current.checked = !checkbox.current.checked
    }
  }
  return (
    <>
      <input
        ref={checkbox}
        name={props.name}
        className='toggle-checkbox'
        type='checkbox'
        defaultChecked={props.value}
        value={(props.value || false).toString()}
      />
      <span
        ref={toggle}
        onClick={handleToggle}
        className={props.checked ? 'toggled toggle-switch' : 'toggle-switch'}
      >
        <span className='toggle'></span>
      </span>
    </>
  )
}