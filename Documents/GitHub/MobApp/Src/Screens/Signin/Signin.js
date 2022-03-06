import {
  View,
  Text,
  Image,
  StyleSheet,
  useWindowDimensions,
  TextInput,
} from "react-native";
import React, { useState } from "react";
import Logo from "../../../assets/logo2.png";
import Custominput from "../../Components/Custominput";
import Custombutton from "../../Components/Custombutton";
import axios from "axios";
import { useNavigation } from "@react-navigation/native";
import { useForm } from "react-hook-form";

const API = "http://localhost:5000";

const Signin = () => {
  const { height } = useWindowDimensions();
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSignInPressed = async (data) => {
    await axios
      .post(`http://192.168.56.1:5000/mobapp`, data)
      .then((resp) => {
        navigation.navigate("Home", { worker: resp.data });
      })
      .catch((err) => alert("Wrong Email or Password"));
  };
  const navigation = useNavigation();
  const onForgotPasswordPressed = () => {
    navigation.navigate("ForgotPassword");
  };
  return (
    <View style={Styles.root}>
      <Image
        source={Logo}
        resizeMode="contain"
        style={(Styles.logo, { height: height * 0.3 })}
      ></Image>
      <Custominput
        rules={{ required: "Email is Required" }}
        placeholder="Email"
        control={control}
        name="email"
      />
      <Custominput
        placeholder="Password"
        name="password"
        rules={{ required: "Password is Required" }}
        control={control}
        secureTextEntry={true}
      />

      <Custombutton
        text="Sign In"
        type="PRIMARY"
        onPress={handleSubmit(onSignInPressed)}
      ></Custombutton>
      <Custombutton
        text="Forgot Password?"
        onPress={onForgotPasswordPressed}
        type="TERTIARY"
      ></Custombutton>
    </View>
  );
};
const Styles = StyleSheet.create({
  root: {
    alignItems: "center",
    padding: 20,
  },
  logo: {
    width: "70%",
    maxWidth: 300,
    maxHeight: 300,
  },
});
export default Signin;
