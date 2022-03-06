import { View, Text } from "react-native";
import React from "react";
import { createMaterialBottomTabNavigator } from "@react-navigation/material-bottom-tabs";
import { NetworkContext } from "../../Context/NetworkContext";

const Home1 = ({ route, navigation }) => {
  const worker = React.useContext(NetworkContext);
  return (
    <View>
      <Text>Home1</Text>
    </View>
  );
};

export default Home1;
