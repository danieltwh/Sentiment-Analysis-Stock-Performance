import Link from 'next/link';
import styles from "./navbar.module.css";
import refresh from '../public/refresh_button.png'
import Image from "next/image";



function Navbar () {
    return (
        <nav className={styles.container}>
            <div className={styles.logo}>
                
                {/* <h1>Sentiment Analysis</h1> */}

            </div>
            <div className="tabs">

                <Link href="/"><button className={styles.buttons}> HOME </button></Link>
                <Link href="/about"><button className={styles.buttons}>ABOUT US</button></Link>
                {/* <span> className={styles.refresh}  */}
                {/* <Image src={refresh} width={50} height={40} />  */}
                {/* </span> */}


                
            </div>
        </nav>
    );
}

export default Navbar;