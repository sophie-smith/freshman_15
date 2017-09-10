import tensorflow as tf
import numpy as np

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label
  
def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph
  
def read_tensor_from_image_file(file_name, input_height=299, input_width=299,
				input_mean=0, input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(file_reader, channels = 3,
                                       name='png_reader')
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                  name='gif_reader'))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
  else:
    image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                        name='jpeg_reader')
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0);
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result

def analyze(file_name):
    #file_name = input("Enter file path: ")
    #file_name = "tf_files/food-101/images/pizza/IMG_7853.jpg"
    model_file = "tf_files/retrained_graph.pb"
    label_file = "tf_files/retrained_labels.txt"
    input_height = 224
    input_width = 224
    input_mean = 128
    input_std = 128
    input_layer = "input"
    output_layer = "final_result"
    '''
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="image to be processed")
    parser.add_argument("--graph", help="graph/model to be executed")
    parser.add_argument("--labels", help="name of file containing labels")
    parser.add_argument("--input_height", type=int, help="input height")
    parser.add_argument("--input_width", type=int, help="input width")
    parser.add_argument("--input_mean", type=int, help="input mean")
    parser.add_argument("--input_std", type=int, help="input std")
    parser.add_argument("--input_layer", help="name of input layer")
    parser.add_argument("--output_layer", help="name of output layer")
    args = parser.parse_args()
    '''
    '''
    
    if args.graph:
        model_file = args.graph
    if args.image:
        file_name = args.image
    if args.labels:
        label_file = args.labels
    if args.input_height:
        input_height = args.input_height
    if args.input_width:
        input_width = args.input_width
    if args.input_mean:
        input_mean = args.input_mean
    if args.input_std:
        input_std = args.input_std
    if args.input_layer:
        input_layer = args.input_layer
    if args.output_layer:
        output_layer = args.output_layer
        '''
    
    graph = load_graph(model_file)
    t = read_tensor_from_image_file(file_name,
                                    input_height=input_height,
                                    input_width=input_width,
                                    input_mean=input_mean,
                                    input_std=input_std)
    
    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name);
    output_operation = graph.get_operation_by_name(output_name);
    
    with tf.Session(graph=graph) as sess:
        results = sess.run(output_operation.outputs[0],
                        {input_operation.outputs[0]: t})
    results = np.squeeze(results)
    
    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(label_file)
    max = 0
    maxfood = ""
    for i in top_k:
        #print(labels[i], results[i])
        if results[i] >= max:
            max = results[i]
            index = i
            maxfood = labels[i]
    maxvalue = np.amax(results)
    return maxfood

dict= { 'apple pie': 67,'baby back ribs': 550, 'breakfast burrito': 340, 'cheesecake': 401, 'chicken quesadilla': 528, "chicken wings": 309, "chocolate cake": 352, "ramen": 188, "hot dog": 151, 'donut': 195, 'waffles': 82}


'''
def askExerciseLevel():
    exerciselevel= input("What is your exercise level? 1) Sedentary(little or no exercise)\2) lightly active(light exercise/sports 1-3 days/week)\3) moderately active(moderate exercise/sports 3-5 days/week)\4) very active(hard exercise/sports 6-7 days a week)\5) extra active(very hard exercise/sports & physical job or 2x training):")
    exerciselevel= int(exerciselevel)
    if exerciselevel== 1:
        exerciselevel= 1.2
    if exerciselevel== 2:
        exerciselevel= 1.375
    if exerciselevel== 3:
        exerciselevel= 1.55
    if exerciselevel== 4:
        exerciselevel= 1.725
    if exerciselevel== 5:
        exerciselevel= 1.9
    return exercise
askExerciseLevel()
'''
    
def dailyCalorieNeeds(age, weight, height, gender, exerciselevel ):
    if exerciselevel== 1:
        exerciselevel= 1.2
    if exerciselevel== 2:
        exerciselevel= 1.375
    if exerciselevel== 3:
        exerciselevel= 1.55
    if exerciselevel== 4:
        exerciselevel= 1.725
    if exerciselevel== 5:
        exerciselevel= 1.9
    if gender == "male" or "Male": 
        dailyCalNeeds= (66 + (6.23 * weight) + (12.7 * height) - (6.8 * age))*exerciselevel
    else:
        dailyCalNeeds= (655 + (4.35 * weight) + (4.7 * height) - (4.7 * age))*exerciselevel
    return int(dailyCalNeeds)


def caloriesBurned():
    print
    filename = input("Path to file: ")
    filename = str(filename)
    age = input("Enter your age: ")
    age = int(age)
    #print(age)
    weight = input("Enter your weight in pounds: " )
    weight = int(int(weight)/2.2)
    weightpounds = int(weight)
    #print(weightpounds)
    height = input("Enter your height in inches: ")
    height = int(height)
    #print(height)
    gender = input("Enter your gender: ")
    gender = str(gender)
    #print(gender)
    activitylevel = input("Activity level from 1-5: ")
    activitylevel = int(activitylevel)
    dailycalorieneeds = dailyCalorieNeeds(age, weightpounds, height, gender, activitylevel)
    biking = 0.0175*8.0*weight
    running = 0.0175*11.0*weight
    swimming = 0.0175*10.0*weight
    walking = 0.0175*3.0*weight
    foodname = str(analyze(filename))
    calories = dict[analyze(filename)]
    print
    print("We identified the food in this picture as being " + foodname + ".")
    print
    calories = int(calories)
    print("Amount of calories in standard serving of " + foodname +": " + str(calories))
    print
    biketime = int(calories/biking)
    runtime = int(calories/running)
    swimtime = int(calories/swimming)
    walktime = int(calories/walking)
    print("It would take " + str(biketime) + " minutes of biking moderately to burn off your " + foodname+".")
    print("It would take " + str(runtime) + " minutes of running at a 9-minute mile pace to burn off your "+ foodname+".")
    print("It would take " + str(swimtime) + " minutes of swimming breaststroke to burn off your "+ foodname+".")
    print("It would take " + str(walktime) + " minutes of walking at a leisurely pace to burn off your "+ foodname +".")
    print
    print("Daily calories needed to maintain weight: " + str(dailycalorieneeds))

caloriesBurned()
    
    
    
