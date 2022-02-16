import React from "react";
import Head from 'next/head'
import Image from 'next/image'
import { TagCloud } from "react-tagcloud";
import styles from '../styles/Home.module.css';
import ButtonSwitcher from "../src/components/ButtonSwitcher";
import http from "../src/http-common";

const users = [
    {
        username: 'gnegrelli_',
        imgUrl: 'https://pbs.twimg.com/profile_images/1403410427095179265/NjkuumlX_400x400.jpg',
    },
    {
        username: 'emicida',
        imgUrl: 'https://pbs.twimg.com/profile_images/1467128299692433411/GkB6v6ky_400x400.jpg',
    },
]

export default function Home() {

    const [ wordCounter, setWordCounter ] = React.useState([]);
    const [ currentUser, setCurrentUser ] = React.useState('')

    function handleButtonClick(props) {
        setCurrentUser(props);
        getTweets(props)
    }

    function getTweets(props) {
        http.get(`/tracker/get-user-tweets/${props}`)
            .then(({ data }) => {
                const lista = Object.entries(data.tokens).map(([token, count]) => (
                    {value: token, count: count}
                ));
                setWordCounter(lista.slice(0, 500));
            })
            .catch((error) => {
                console.log(error);
                setWordCounter([]);
            })
    }

    return (
        <div className={styles.container}>
            <Head>
                <title>Tweet Tracker</title>
                <meta name="description" content="Generated by create next app"/>
                <link rel="icon" href="/favicon.ico"/>
            </Head>

            <main className={styles.main}>
                <h1 className={styles.title}>
                    Tweet Tracker
                </h1>
                <p className={styles.description}>
                    {currentUser ?
                        `Showing tweets made by @${currentUser}` :
                        "Select user clicking on one of the buttons below"
                    }
                </p>

                <TagCloud className={styles.tagcloud} tags={wordCounter} minSize={1} maxSize={50} shuffle={false} />

                <ButtonSwitcher imageObjs={users} onButtonClick={handleButtonClick} />

            </main>

            {/*<footer className={styles.footer}>*/}
            {/*    <a*/}
            {/*        href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"*/}
            {/*        target="_blank"*/}
            {/*        rel="noopener noreferrer"*/}
            {/*    >*/}
            {/*        Powered by{' '}*/}
            {/*        <span className={styles.logo}>*/}
            {/*            <Image src="/vercel.svg" alt="Vercel Logo" width={72} height={16}/>*/}
            {/*        </span>*/}
            {/*    </a>*/}
            {/*</footer>*/}
        </div>
    )
}
