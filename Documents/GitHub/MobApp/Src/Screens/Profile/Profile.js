import React from "react";
import { useEffect } from "react";
import axios from "axios";
import { createMaterialBottomTabNavigator } from "@react-navigation/material-bottom-tabs";
import { NetworkContext } from "../../Context/NetworkContext";
import {
  StyleSheet,
  Text,
  SafeAreaView,
  Image,
  TouchableOpacity,
} from "react-native";
const Profile = ({ route, navigation }) => {
  const worker = React.useContext(NetworkContext);
  return (
    <SafeAreaView style={styles.container}>
      <SafeAreaView style={styles.header}></SafeAreaView>
      <Image
        style={styles.avatar}
        source={{ uri: "https://bootdey.com/img/Content/avatar/avatar6.png" }}
      />
      <SafeAreaView style={styles.body}>
        <SafeAreaView style={styles.bodyContent}>
          <Text style={styles.name}>{worker.worker.fName}</Text>
          <Text style={styles.info}>{worker.worker.ID}</Text>
          <Text style={styles.description}>Age: {worker.worker.age}</Text>
          <Text style={styles.description}>Email: {worker.worker.email}</Text>
          <Text style={styles.description}>
            Phone Number: {worker.worker.phoneNumber}
          </Text>

          <TouchableOpacity style={styles.buttonContainer}>
            <Text>Opcion 1</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.buttonContainer}>
            <Text>Opcion 2</Text>
          </TouchableOpacity>
        </SafeAreaView>
      </SafeAreaView>
    </SafeAreaView>
  );
};
const styles = StyleSheet.create({
  header: {
    backgroundColor: "#00BFFF",
    height: 200,
  },
  avatar: {
    width: 130,
    height: 130,
    borderRadius: 63,
    borderWidth: 4,
    borderColor: "white",
    marginBottom: 10,
    alignSelf: "center",
    position: "absolute",
    marginTop: 130,
  },
  name: {
    fontSize: 22,
    color: "#FFFFFF",
    fontWeight: "600",
  },
  body: {
    marginTop: 40,
  },
  bodyContent: {
    alignItems: "center",
    padding: 30,
  },
  name: {
    fontSize: 28,
    color: "#696969",
    fontWeight: "600",
  },
  info: {
    fontSize: 16,
    color: "#00BFFF",
    marginTop: 10,
  },

  description: {
    fontSize: 16,
    color: "#696969",
    marginTop: 10,
    textAlign: "center",
  },
  buttonContainer: {
    marginTop: 10,
    height: 45,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 20,
    width: 250,
    borderRadius: 30,
    backgroundColor: "#00BFFF",
  },
});
export default Profile;
