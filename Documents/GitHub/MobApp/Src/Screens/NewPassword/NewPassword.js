import { View, Text, StyleSheet } from "react-native";
import React from "react";
import Custombutton from "../../Components/Custombutton";
import Custominput from "../../Components/Custominput";
import { useForm } from "react-hook-form";
import axios from "axios";

const NewPassword = ({ route, navigation }) => {
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const email = route.params;

  const onChangePasswordPressed = async (data) => {
    if (String(data.password1) !== String(data.password2)) {
      alert("The password dont match");
      return;
    }
    const user = {
      email: "",
      password: "",
    };
    user.email = email.email;
    user.password = data.password1;
    console.log(user);
    await axios
      .post(`http://192.168.56.1:5000/mobapp/reset`, user)
      .then((resp) => {
        navigation.navigate("Home", {
          worker: resp.data,
        });
      })
      .catch((err) => alert("The code is not correct"));
  };
  return (
    <View style={Styles.root}>
      <Text style={Styles.title}>Change your password</Text>
      <Custominput
        placeholder={"Chosse new password"}
        control={control}
        name="password1"
        secureTextEntry={true}
        rules={{ required: "Password is Required" }}
      />
      <Custominput
        placeholder={"Confirm your password"}
        control={control}
        secureTextEntry={true}
        rules={{ required: "Confirm password is Required" }}
        name="password2"
      />

      <Custombutton
        text="Change Password"
        onPress={handleSubmit(onChangePasswordPressed)}
        type="SECONDARY"
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
  title: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#051c60",
    margin: 10,
  },
});

export default NewPassword;
