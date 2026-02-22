package ru.morzevichka.auth_service.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.morzevichka.auth_service.dto.UserRegisterDto;
import ru.morzevichka.auth_service.exception.user.UserAlreadyExistsException;
import ru.morzevichka.auth_service.exception.user.UserNotFoundException;
import ru.morzevichka.auth_service.model.user.Role;
import ru.morzevichka.auth_service.model.user.User;
import ru.morzevichka.auth_service.repository.UserRepository;

import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public User getByEmail(String email) {
        return userRepository.findByEmail(email)
                .orElseThrow(() -> new UserNotFoundException(email));
    }

    public User getById(UUID id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException(id.toString()));
    }

    public boolean existsByEmail(String email) {
        return userRepository.existsByEmail(email);
    }

    public boolean existsByLogin(String login) {
        return userRepository.existsByLogin(login);
    }

    @Transactional
    public User register(UserRegisterDto dto) {
        if (existsByEmail(dto.email())) {
            throw new UserAlreadyExistsException(dto.email() + " is already exists");
        }

        if (existsByLogin(dto.login())) {
            throw new UserAlreadyExistsException(dto.login() + " is already taken");
        }

        User user = User.builder()
                .login(dto.login())
                .email(dto.email())
                .passwordHash(passwordEncoder.encode(dto.password()))
                .role(Role.ROLE_USER)
                .build();

        user = userRepository.save(user);

        return user;
    }
}
