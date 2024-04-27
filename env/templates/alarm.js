import styles from "./Alarm.module.css";

const Alarm = () => {
  return (
    <div className={styles.alarm}>
      <div className={styles.vectorParent}>
        <img className={styles.vectorParent} alt="" src="/rectangle-5.svg" />
        <div className={styles.frameItem} />
        <div className={styles.frameInner} />
        <div className={styles.rectangleDiv} />
        <div className={styles.totalTime}>Total Time</div>
        <div className={styles.mins}>30 mins</div>
      </div>
      <div className={styles.vectorGroup}>
        <img className={styles.vectorParent} alt="" src="/rectangle-51.svg" />
        <div className={styles.frameChild1} />
        <div className={styles.frameChild2} />
        <div className={styles.frameChild3} />
        <div className={styles.setYourAlarm}>Set Your Alarm</div>
        <div className={styles.frameChild4} />
        <div className={styles.frameChild5} />
        <b className={styles.set}>Set</b>
        <b className={styles.setYourEmail}>Set Your Email</b>
        <b className={styles.hours}>Hours</b>
        <b className={styles.minutes}>Minutes</b>
        <div className={styles.frameChild6} />
        <b className={styles.b}>00</b>
        <b className={styles.xyzmegmailcom}>xyzme@gmail.com</b>
        <b className={styles.b1}>03</b>
      </div>
      <img className={styles.alarmChild} alt="" src="/rectangle-6.svg" />
      <img className={styles.house1Icon} alt="" src="/house-1@2x.png" />
      <img className={styles.alarm1Icon} alt="" src="/alarm-1@2x.png" />
      <img className={styles.bar1Icon} alt="" src="/bar-1@2x.png" />
      <img className={styles.pomodoro1Icon} alt="" src="/pomodoro-1@2x.png" />
      <div className={styles.alarmItem} />
      <img
        className={styles.exit16291881Icon}
        alt=""
        src="/exit-1629188-1@2x.png"
      />
      <b className={styles.tracksense}>TrackSense</b>
      <b className={styles.setAlarmNotification}>Set Alarm Notification</b>
      <div className={styles.alarmInner} />
      <div className={styles.search}>Search</div>
      <img className={styles.searchIcon} alt="" src="/search@2x.png" />
      <img
        className={styles.testAccountIcon}
        alt=""
        src="/test-account@2x.png"
      />
    </div>
  );
};

export default Alarm;
