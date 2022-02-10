import React from "react";
import { Avatar, IconButton, Stack } from "@mui/material";

const ButtonContext = React.createContext({});

export default function ButtonSwitcher (props) {
    const [ activeButton, setActiveButton ] = React.useState();

    return (
        <ButtonContext.Provider value={[activeButton, setActiveButton]}>
            <Stack direction="row" spacing={1} >
                {props.images.map((image) => (
                    <MyIconButton
                        key={image.title}
                        image={image}
                        // onButtonClick={props.onButtonClick}
                    />
                ))}
            </Stack>
        </ButtonContext.Provider>
    );
}

function MyIconButton({ image, onButtonClick }) {

    const [ activeButton, setActiveButton ] = React.useContext(ButtonContext);
    const [ isButtonColored, setIsButtonColored ] = React.useState(false);

    React.useEffect(() => {
        activeButton === image.title ? setIsButtonColored(true) : setIsButtonColored(false);
    }, [activeButton]);

    function handleClickEvent(event) {
        // const words = [
        //     {
        //         text: 'asdrubal',
        //         value: 17,
        //     },
        // ];
        // onButtonClick(words);
        console.log(activeButton);
        console.log(event.target.parentElement);
        // console.log(event.target.offsetParent);
        // console.log(event.target.offsetParent.value);
    }


    return (
        <IconButton
            onClick={(event) => {
                setActiveButton(image.title);
                handleClickEvent(event);
            }}
            onMouseEnter={() => setIsButtonColored(true)}
            onMouseLeave={() => activeButton === image.title || setIsButtonColored(false)}
        >
            <Avatar
                value={image.title}
                src={image.url}
                style={{
                    filter: isButtonColored ? 'none' : 'grayscale(1)',
                    width: "60px",
                    height: "60px",
                }}
            />
        </IconButton>
    )
}