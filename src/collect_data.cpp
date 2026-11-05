#include <iostream>
#include <fstream>

#include <iomanip>
#include <vector>
#include <rclcpp/rclcpp.hpp>
#include <rfid_sensor/msg/tag_array.hpp>

std::vector<std::ofstream> value_files;
int count = 0;

void rfid_callback(const rfid_sensor::msg::TagArray::ConstSharedPtr &data, int index) {

	for (int i = 0; i < data->ntags; i++) 
	{
        value_files[index] << data->header.stamp.sec << "."
                           << std::setfill('0') << std::setw(9) << data->header.stamp.nanosec
                           << "," << data->antenna_pose.position.x
                           << "," << data->antenna_pose.position.y
                           << "," << data->antenna_pose.position.z
                           << "," << data->antenna_pose.orientation.x
                           << "," << data->antenna_pose.orientation.y
                           << "," << data->antenna_pose.orientation.z
                           << "," << data->antenna_pose.orientation.w
                           << "," << data->tags[i].name << "," << data->tags[i].dist
                           << "," << data->tags[i].phi << "," << data->tags[i].rssi << std::endl;
	}
}

int main(int argc, char** argv) {
    const auto arguments = rclcpp::init_and_remove_ros_arguments(argc, argv);
    argc = static_cast<int>(arguments.size());
	if (argc < 2) {
        std::cerr << "Usage: " << arguments[0] << " /gazebo/antenna1_robot/data" << std::endl;
        return 1;
    }

	auto nh = std::make_shared<rclcpp::Node>("collect_data");

	std::vector<rclcpp::Subscription<rfid_sensor::msg::TagArray>::SharedPtr> subscribers;

	for (int i = 0; i < argc-1; i++)
	{
		rclcpp::Subscription<rfid_sensor::msg::TagArray>::SharedPtr sub;
		subscribers.push_back(sub);
		std::ofstream file;
		std::string input = arguments[i+1];
		std::string app = input.substr(input.find_first_of("/") + 1);
		int first = app.find_first_of("/");
		int last = app.find_last_of("/");
		std::string antenna_name = app.substr(first + 1, last-first-1);
		file.open(antenna_name + ".csv");
		value_files.push_back(std::move(file));
		value_files[i] << "time" << "," << "posx" << "," << "posy" << "," << "posz" << "," << 
						"q1" << "," << "q2" << "," << "q3" << "," << "q4"
						<< "," << "name" << "," << "dist" << "," << "fase" << "," << "rssi" << std::endl;
	}

    for (int i = 0; i < argc-1; i++) {
        subscribers[i] = nh->create_subscription<rfid_sensor::msg::TagArray>(
            arguments[i+1],
            rclcpp::QoS(10),
            [i](rfid_sensor::msg::TagArray::ConstSharedPtr data) {
                rfid_callback(data, i);
            }
        );
    }

    rclcpp::spin(nh);

	for (int i = 0; i < argc-1; i++)
		value_files[i].close();

	rclcpp::shutdown();
}