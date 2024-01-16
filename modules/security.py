import cv2
import os
from skimage.metrics import mean_squared_error
import shutil
import time
from conversation import openai_chat

# Constants
FACE_CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
OUTPUT_FOLDER = 'FaceData'
MAX_IMAGES = 100
THRESHOLD_MSE = 500
USERS_FILE = 'users.txt'

def load_user_data(file_path):
    if not os.path.exists(file_path):
        # Tạo file nếu nó không tồn tại
        with open(file_path, 'w'):
            pass
    user_data = []
    with open(file_path, 'r') as file:
        for line in file:
            user_data.append(line.strip().split())
    return user_data

def save_user_data(file_path, username, face_data_path):
    with open(file_path, 'a') as file:
        file.write(f"{username} {face_data_path}\n")

def delete_user_data(username):
    user_folder = os.path.join(OUTPUT_FOLDER, username)
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)
        print(f"Data for user {username} deleted successfully.")
        # Xóa người dùng khỏi tệp users.txt
        user_data = load_user_data(USERS_FILE)
        user_data = [user for user in user_data if user[0] != username]
        with open(USERS_FILE, 'w') as file:
            for user in user_data:
                file.write(f"{user[0]} {user[1]}\n")
        print(f"User {username} removed from {USERS_FILE}.")
    else:
        print(f"No data found for user {username}.")

def delete_all_data():
    if os.path.exists(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)
        os.makedirs(OUTPUT_FOLDER)
        print("All data deleted successfully.")
        # Xóa tệp users.txt nếu tồn tại
        users_file_path = os.path.join(os.getcwd(), USERS_FILE)
        if os.path.exists(users_file_path):
            os.remove(users_file_path)
            print(f"{USERS_FILE} deleted successfully.")
    else:
        print("No data found to delete.")

def load_reference_images(folder_path):
    reference_images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            reference_image_path = os.path.join(folder_path, filename)
            reference_image = cv2.imread(reference_image_path, cv2.IMREAD_GRAYSCALE)
            reference_images.append(reference_image)
    return reference_images

def save_face_image(face_image, output_folder, username, index):
    user_folder = os.path.join(output_folder, username)
    os.makedirs(user_folder, exist_ok=True)
    image_path = os.path.join(user_folder, f'face_{index}.jpg')
    cv2.imwrite(image_path, face_image)
    return image_path

def capture_and_save_images(output_folder, max_images, username):
    image_count = 0
    cap = cv2.VideoCapture(0)

    while image_count < max_images:
        ret, frame = cap.read()

        if not ret:
            print("ERROR: Failed to capture frame from the camera. Exiting...")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            if h > 0 and w > 0:
                face_image = cv2.resize(gray[y:y+h, x:x+w], (w, h))
                image_path = save_face_image(face_image, output_folder, username, image_count)
                image_count += 1
                print(image_count, "%")

        cv2.imshow('Capture Images', frame)

        if cv2.waitKey(1) == ord('q') or image_count >= max_images:
            break

    cap.release()
    cv2.destroyAllWindows()

    print(f"Done! Please exit the program and login with your face!")

def login_with_face(face_cascade, reference_images, threshold_mse, user_data_name, username):
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("ERROR: Failed to capture frame from the camera. Exiting...")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            if h > 0 and w > 0:
                face_image = cv2.resize(gray[y:y+h, x:x+w], (w, h))

                for i, user in enumerate(user_data_name):
                    stored_username, _ = user
                    if stored_username == username:
                        # Only compare with reference images of the specific user
                        user_reference_images = load_reference_images(os.path.join(OUTPUT_FOLDER, stored_username))
                        for reference_image in user_reference_images:
                            resized_reference_image = cv2.resize(reference_image, (face_image.shape[1], face_image.shape[0]))
                            mse = mean_squared_error(resized_reference_image, face_image)

                            if mse < threshold_mse:
                                print(f"Match!")
                                time.sleep(3)

                                cap.release()
                                cv2.destroyAllWindows()
                                openai_chat()
                                return  # Thoát khỏi hàm

        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def register_user():
    print("Register a new user:")
    username = input("Enter your username: ")
    # Check if username already exists
    user_data = load_user_data(USERS_FILE)
    existing_usernames = [user[0] for user in user_data]
    while username in existing_usernames:
        print("Username already exists. Please choose a different username.")
        username = input("Enter your username: ")

    face_data_path = os.path.join(OUTPUT_FOLDER, username, f'{username}_face_data.jpg')

    # Capture face data
    capture_and_save_images(OUTPUT_FOLDER, MAX_IMAGES, username)

    # Save user information to the users.txt file
    save_user_data(USERS_FILE, username, face_data_path)

    print("User registered successfully!")

if __name__ == "__main__":
    # Load face cascade classifier
    face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)

    # Check if the output folder exists, if not, create it
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Choose an option: Register (1), Login (2), Delete User (3)
    print("Choose an option:")
    print("1. Register")
    print("2. Login")
    print("3. Delete User")

    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == '1':
        # Register a new user
        register_user()
    elif choice == '2':
        # Login with existing face data
        username = input("Enter your username: ")
        user_data_name = load_user_data(USERS_FILE)
        if any(username in user for user in user_data_name):
            reference_images = load_reference_images(os.path.join(OUTPUT_FOLDER, username))
            login_with_face(face_cascade, reference_images, THRESHOLD_MSE, user_data_name, username)
        else:
            print("User not found.")
    elif choice == '3':
        delete_choice = input("Do you want to delete data for a specific user or all users? (user/all): ")
        if delete_choice.lower() == 'user':
            delete_username = input("Enter the username to delete: ")
            delete_user_data(delete_username)
        elif delete_choice.lower() == 'all':
            delete_all_data()
        else:
            print("Invalid choice.")
    else:
        print("Invalid choice. Please enter either '1', '2', or '3'.")
