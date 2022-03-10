import React from "react";
import { Avatar, IconButton, Stack } from "@mui/material";

const ButtonContext = React.createContext({});

export default function ButtonSwitcher (props) {
    const [ activeButton, setActiveButton ] = React.useState();

    return (
        <ButtonContext.Provider value={[activeButton, setActiveButton]}>
            <Stack direction="row" spacing={1} >
                {props.imageObjs.map((imageObj) => (
                    <MyIconButton
                        key={imageObj.username}
                        imageObj={imageObj}
                        onButtonClick={props.onButtonClick}
                    />
                ))}
            </Stack>
        </ButtonContext.Provider>
    );
}

function MyIconButton({ imageObj, onButtonClick }) {

    const [ activeButton, setActiveButton ] = React.useContext(ButtonContext);
    const [ isButtonColored, setIsButtonColored ] = React.useState(false);

    const username = imageObj.username;

    React.useEffect(() => {
        activeButton === username ? setIsButtonColored(true) : setIsButtonColored(false);
    }, [activeButton]);

    function handleClickEvent() {
        username !== activeButton ? onButtonClick(username) : null;
    }

    return (
        <IconButton
            onClick={() => {
                handleClickEvent();
                setActiveButton(username);
            }}
            onMouseEnter={() => setIsButtonColored(true)}
            onMouseLeave={() => activeButton === username || setIsButtonColored(false)}
        >
            <Avatar
                value={username}
                src={imageObj.imgUrl}
                style={{
                    filter: isButtonColored ? 'none' : 'grayscale(1)',
                    width: "65px",
                    height: "65px",
                }}
            />
        </IconButton>
    )
}