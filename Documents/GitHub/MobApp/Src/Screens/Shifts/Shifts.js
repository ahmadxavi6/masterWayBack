import { View, Text } from "react-native";
import React from "react";
import { createMaterialBottomTabNavigator } from "@react-navigation/material-bottom-tabs";
import { NetworkContext } from "../../Context/NetworkContext";

const Shifts = ({ route, navigation }) => {
  const worker = React.useContext(NetworkContext);
  return (
    <View>
      <Text>Shifts</Text>
    </View>
  );
};

export default Shifts;
