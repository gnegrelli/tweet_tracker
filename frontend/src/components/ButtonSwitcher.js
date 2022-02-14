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
                        onButtonClick={props.onButtonClick}
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

    function handleClickEvent(imageTitle) {
        imageTitle !== activeButton ? onButtonClick(imageTitle) : null;
    }


    return (
        <IconButton
            onClick={() => {
                handleClickEvent(image.title);
                setActiveButton(image.title);
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