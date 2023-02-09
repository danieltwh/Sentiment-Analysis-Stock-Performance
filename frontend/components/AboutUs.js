import React from "react";
// import styles from "../styles/Home.module.css";
import styles from "./AboutUs.module.css";

import Image from "next/image";

export default function AboutUs() {
    return ( 
        <div className={styles.aboutDiv}> 
              <h1> SENTIMENT ANALYSIS </h1>
              <br></br>
              <p>This web app is to display Sentiment Analysis Stock Performance </p>;


        </div>
    )
}